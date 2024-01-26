import os
import re
import glob
import argparse
import shutil
import subprocess

# Parser setup
parser = argparse.ArgumentParser(description="Compile and grade cpp files")
parser.add_argument("-r", "--recompile", help="force recompile files", action="store_true")
parser.add_argument("-t", "--timeout", help="set the timeout in seconds (default: 5)", type=int, default=5)
args = parser.parse_args()

# Directory variables
src_directory = "cpp"
exe_directory = "exe"
test_directory = "tests"
results_directory = "results"

# Determine which compiler to use
compiler = None
if shutil.which("g++") is not None:
    compiler = "g++"
elif shutil.which("clang++") is not None:
    compiler = "clang++"
else:
    raise Exception("Missing compiler: install g++ or clang++")


# Compile all the files in the src directory
print("Compilation start")

for src_path in glob.glob(f"{src_directory}/*.cpp"):
    basename = os.path.basename(src_path)[:-4] # get filename w/o extension

    exe_path = f"{exe_directory}/{basename}.exe" 

    # perform compilation on the commandline
    if args.recompile or not os.path.exists(exe_path):
        os.system(f'{compiler} -Wall -o {exe_path} {src_path}')

print("Compilation complete\n")

# Execute the programs
print("Execution start")

for exe_path in glob.glob(f"{exe_directory}/*.exe"):
    basename = os.path.basename(exe_path)[:-4] # get filename w/o extension

    problem_match = re.search(r"P\d", exe_path) # get the problem number from the file name
    
    if not problem_match:
        print(f"MISSING PROBLEM NUMBER: {basename}.cpp")
        continue

    problem = problem_match.group(0)
    
    # Run every test case for this problem
    for test_case_path in glob.glob(f"{test_directory}/{problem}*.in"):
        test_case_match = re.search(r"(P\d\_.+).in", test_case_path)
        test_case_name = test_case_match.group(1)
        output_filename = f"{results_directory}/{basename}_{test_case_name}.out"
        
        # Open I/O and run program
        with open(test_case_path, "r") as input_file:
            with open(output_filename, "w") as output_file:
                try:
                    subprocess.run(exe_path, stdin = input_file, stdout = output_file, timeout=args.timeout)
                except subprocess.TimeoutExpired:
                    print(f"TIMED OUT: {basename}.cpp ({test_case_name})")
                    output_file.write("<TIMEOUT>")
            
print("Execution complete")



    
