import os
import re
import glob
import argparse

parser = argparse.ArgumentParser(description="Compile and grade cpp files")
parser.add_argument("-r", "--recompile", help="force recompile files", action="store_true")
args = parser.parse_args()

src_directory = "cpp"
exe_directory = "exe"

print("Compilation start")

# Compile all the files in the src directory
for path in glob.glob(f"{src_directory}/*.cpp"):
    basename = os.path.basename(path)[:-4] # get filename w/o extension

    executable_path = f"{exe_directory}/{basename}.exe" 

    # perform compilation on the commandline
    if args.recompile or not os.path.exists(executable_path):
        os.system(f'g++ -Wall {path} -o {executable_path}')

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
            os.system(f"{path} < {test_case} > results/{basename}_{test_case_name}.out")
            
    else:
        print(f"MISSING PROBLEM NUMBER: {basename}.cpp")

print("Execution complete")



    
