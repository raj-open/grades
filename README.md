# Grades #

This is a small python package with a few methods via which one can read in csv files
and produce plots of distributions of grades.

## Quick guide to usage ##

You need at least `python 3.10`. Install the package via

```bash
python3 -m pip install git+https://github.com/raj-open/grades.git@main
```

Use the package as follows:

```py
from r_open_grades import *;
case = Case(
    path_input = 'path/to/your/data.csv',
    path_output = 'path/to/desired/output.png',
    # use intellisense to see other required/optional arguments
    ...
);
run(case);
```

See [examples/README.md](examples/README.md) for more information
and [examples/example.py](examples/example.py) for a full example.
