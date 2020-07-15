import datetime
import time
import threading

from IPython.core.magic import register_line_magic, register_line_cell_magic


def shortentxt(txt, maxlen=20):
    txt = txt.splitlines()[0]
    if len(txt) > 20:
        txt = txt[:17] + "..."
    return txt


def runjob(ipython, lock, jobrow, code):
    try:
        exec(code, ipython.user_ns)
    except Exception as e:
        res = ["exception", e]
        raise
    else:
        res = ["done"]
    finally:
        now = datetime.datetime.now()
        with lock:
            jobrow.extend(res + [now])
        print("[job completed]", shortentxt(code))


lock = threading.Lock()
jobslist = []
        

def load_ipython_extension(ipython):
    @register_line_cell_magic
    def bg(line, cell=None):
        code = cell or line
        if not code.strip(): return
        with lock:
            jobrow = [datetime.datetime.now(), code]
            thread = threading.Thread(target=runjob, args=(ipython, lock, jobrow, code))
            jobrow.append(thread)
            jobslist.append(jobrow)
            thread.start()

    @register_line_magic
    def jobs(line):
        with lock:
            if not jobslist:
                print("no jobs")
                return
            print("jobs:")
            for start, code, thread, *more in jobslist:
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
                print(f"start={start:%H:%M:%S}, code={shortentxt(code)}{more}")

                
if __name__ == "__main__":
    from IPython import get_ipython
    load_ipython_extension(get_ipython())
