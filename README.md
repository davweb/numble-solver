# numble-solver
This is a Python script to solve [Numble](https://numble.wtf) puzzles.  I wrote when I couldn't solve the puzzle one day and decided if I wrote a solver script myself then it still counted.

The script will return a single solution to the puzzle or report if a solution cannot be found.  It just returns the first solution it finds.  This is not necessarily the best solution (for whatever your definition of "best" is here).

## How to Use
Run the `numble_solver.py` script on the command line, passing in the target number as the first argument and all the source numbers remaining arguments.

A successful example:

    ```
    $ python numble_solver.py 741 100 3 5 7 10 25 100
    100 - 25 = 75
    75 × 10 = 750
    750 - 7 = 743
    743 - 5 = 738
    738 + 3 = 741
    ```

An unsuccessful example:

    ```
    $ python numble_solver.py 733 2 4 5 10 25 100
    No solution found.
    ```

## Requirements
The requirements are only used for development.  You can install them as follows.

1. Set up a python virtual environment with:

    ```
    python -m venv --prompt numble-solver .venv
    ```

2. Source the virtual environment with:

    ```
    source .venv/bin/activate
    ```

3. Install required packages using `pip`:

    ```
    pip install pip-tools
    pip-compile requirements.in
    pip-sync
    ```

This will allow you to use `pytest`, `pylint`, `mypy` and `autopep8` to validate the code.
