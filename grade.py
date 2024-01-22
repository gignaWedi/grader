import os
import re
import glob

os.system("compile")

exe_directory = "exe"

for filename in os.listdir(exe_directory):
    fullname = os.path.join(exe_directory, filename)

    m = re.search(r"(P\d)", fullname)
    
    if m:
        problem = m.group(0)
        
        for test_case in glob.glob(f"tests/{problem}*.in"):
            
            m2 = re.search(r"P\d\_(\d+)", test_case)

            num = m2.group(0)
            os.system(f"{fullname} < {test_case} > results/{filename[:-4]}_{num}.out")
            
    else:
        print(f"missing problem number: {filename}")



    
