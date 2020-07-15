# ipython-bg

1. Use `%bg ...` to run line in background
2. Use `%%bg` to run cell in background
3. Use `%jobs` to view all background jobs

```
In [1]: %load_ext ipython_bg

In [2]: %bg run_this_command_in_background = 1

[job completed] run_this_command_...
In [3]: %jobs
jobs:
start=19:21:04, code=run_this_command_..., done, finished=19:21:04, took=0:0

In [4]: %%bg 
   ...: run_this_cell_in_background = 1 
   ...: more_lines = "yes, more lines." 
   ...:

[job completed] run_this_cell_in_...
In [5]: %jobs
jobs:
start=19:21:04, code=run_this_command_..., done, finished=19:21:04, took=0:0
start=19:21:29, code=run_this_cell_in_..., done, finished=19:21:29, took=0:0

In [6]: print(run_this_command_in_background, run_this_cell_in_background, more_lines)
1 1 yes, more lines.
```