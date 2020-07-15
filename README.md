# ipython-bg

1. Use `%bg` to run line in background
2. Use `%%bg` to run cell in background
3. Use `%jobs` to view all background jobs
4. Use `%kill` to try to kill a thread - only works if thread runs python code

## How to load extension
```
In [1]: %load_ext ipython_bg
```

## %bg - run line in background
```
In [2]: %bg run_this_command_in_background = 1
[1] running in background

[job completed] run_this_command_...
```

## %%bg - run cell in background
```
In [3]: %%bg 
   ...: run_this_cell_in_background = 1 
   ...: more_lines = "yes, more lines." 
   ...:  
   ...:
   
[2] running in background

[job completed] run_this_cell_in_...
```

## %jobs - view all background jobs
```
In [4]: %jobs
jobs:
[1] start=22:49:50, code=run_this_command_..., completed, finished=22:49:50, took=0:0
[2] start=22:50:13, code=run_this_cell_in_..., completed, finished=22:50:13, took=0:0

In [5]: print(run_this_command_in_background, run_this_cell_in_background, more_lines)
1 1 yes, more lines.
```

## %kill - try to kill a thread
```
In [6]: %%bg 
   ...: import time 
   ...: time.sleep(5) 
   ...: print("this won't be printed :(") 
   ...: time.sleep(100000) 
   ...:

[3] running in background

In [7]: %kill 3
[job killed] import time...
Exception in thread Thread-4:
Traceback (most recent call last):
  File "/Users/drorspei/.pyenv/versions/3.6.10/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "/Users/drorspei/.pyenv/versions/3.6.10/lib/python3.6/threading.py", line 864, in run
    self._target(*self._args, **self._kwargs)
  File "/Users/drorspei/src/ipython-bg/ipython_bg/__init__.py", line 19, in runjob
    exec(code, ipython.user_ns)
  File "<string>", line 2, in <module>
KeyboardInterrupt
```