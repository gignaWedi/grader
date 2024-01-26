# grader

Handles batch compiling and executing of cpp files for grading purposes. 

Requires python 3.7+ and g++ or clang++.

## Usage:

1. Put all `.cpp` files in the `cpp/` directory
2. Put all test case input files in tests (format: `P#_testcasename.in`, where # is the corresponding problem number)
3. Run the script `python grade.py`
4. Results will be stored in the `results/` directory 

### Options:
`-r, --recompile` force recompile cpp files
`-t TIMEOUT, --timeout TIMEOUT` set the timeout for each execution in seconds (defaults to 5)

