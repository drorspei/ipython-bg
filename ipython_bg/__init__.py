import ctypes
import datetime
import time
import threading

from IPython.core.magic import register_line_magic, register_line_cell_magic


def shortentxt(txt, maxlen=20):
    lines = txt.splitlines()
    if len(lines) > 1:
        txt = lines[0] + "..."
    if len(txt) > maxlen:
        txt = txt[:maxlen - 3] + "..."
    return txt


def runjob(ipython, lock, jobrow, code):
    res = ["killed"]
    try:
        exec(code, ipython.user_ns)
    except Exception as e:
        res = ["through exception", e]
        raise
    else:
        res = ["completed"]
    finally:
        now = datetime.datetime.now()
        with lock:
            jobrow.extend(res + [now])
        print(f"[job {res[0]}]", shortentxt(code))


lock = threading.Lock()
jobslist = []
        

def load_ipython_extension(ipython):
    @register_line_cell_magic
    def bg(line, cell=None):
        code = cell or line
        if not code.strip(): return
        with lock:
            jobrow = [datetime.datetime.now(), code]
            thread = threading.Thread(
                target=runjob, args=(ipython, lock, jobrow, code)
            )
            jobrow.append(thread)
            jobslist.append(jobrow)
            print(f"[{len(jobslist)}] running in background")
            thread.start()

    @register_line_magic
    def jobs(line):
        with lock:
            if not jobslist:
                print("no jobs")
                return
            print("jobs:")
            for i, (start, code, thread, *more) in enumerate(jobslist):
                if more:
                    finished = more[-1]
                    minutes, seconds = divmod(
                        (finished - start).total_seconds(),
                        60
                    )
                    more = (
                        "".join(f", {m}" for m in more[:-1]) +
                        f", finished={finished:%H:%M:%S}"
                        f", took={int(minutes)}:{int(seconds)}"
                    )
                else:
                    more = ''
                print(
                    f"[{i + 1}] start={start:%H:%M:%S}"
                    f", code={shortentxt(code)}{more}"
                )

    @register_line_magic
    def kill(line):
        try:
            jobid = int(line.strip()) - 1
        except Exception:
            print("couldn't parse job number")
            return
        
        with lock:
            if len(jobslist) <= jobid or jobid < 0:
                print("job number doesn't exist")
                return
            
            if len(jobslist[jobid]) > 3:
                print("job not running")
                return
            
            thread = jobslist[jobid][2]
            
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_ulong(thread.ident),
            ctypes.py_object(KeyboardInterrupt)
        )
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, 0)

                
if __name__ == "__main__":
    from IPython import get_ipython
    load_ipython_extension(get_ipython())
