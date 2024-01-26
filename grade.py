import os
import re
import glob
import argparse
import shutil
import subprocess

parser = argparse.ArgumentParser(description="Compile and grade cpp files")
parser.add_argument("-r", "--recompile", help="force recompile files", action="store_true")
args = parser.parse_args()

compiler = None
if shutil.which("g++") is not None:
    compiler = "g++"
elif shutil.which("clang++") is not None:
    compiler = "clang++"
else:
    raise Exception("Missing compiler: install g++ or clang++")


src_directory = "cpp"
exe_directory = "exe"
TIMEOUT = 5

print("Compilation start")

# Compile all the files in the src directory
for path in glob.glob(f"{src_directory}/*.cpp"):
    basename = os.path.basename(path)[:-4] # get filename w/o extension

    executable_path = f"{exe_directory}/{basename}.exe" 

    # perform compilation on the commandline
    if args.recompile or not os.path.exists(executable_path):
        os.system(f'{compiler} -Wall -o {executable_path} {path}')

print("Compilation complete\n")

print("Execution start")

# Execute the programs
for path in glob.glob(f"{exe_directory}/*.exe"):
    basename = os.path.basename(path)[:-4] # get filename w/o extension

    problem_match = re.search(r"P\d", path) # get the problem number from the file name
    
    if problem_match:
        problem = problem_match.group(0)
        
        for test_case in glob.glob(f"tests/{problem}*.in"):
            test_case_match = re.search(r"(P\d\_.+).in", test_case)

            test_case_name = test_case_match.group(1)
            
            with open(test_case, "r") as input_file:
                with open(f"results/{basename}_{test_case_name}.out", "w") as output_file:
                    try:
                        subprocess.run(path, stdin = input_file, stdout = output_file, timeout=TIMEOUT)
                    except subprocess.TimeoutExpired:
                        print(f"TIMED OUT: {basename}.cpp ({test_case_name})")
                        output_file.write("<TIMEOUT>")
            
    else:
        print(f"MISSING PROBLEM NUMBER: {basename}.cpp")

print("Execution complete")



    
