import json
import sys
import os
import traceback
import shutil
import re



"""
 This script reads all the logs files in Results/Pending, 
 possibly fixing any json error, and then extracts all the ILP executions.
 For each instance execution in ILP, it gets the time, the filename of the instance and if it got time limit, and then moves the instance file to the Instances/Final/ folder with a name like this:
    0124-<instance>.dat
"""

results_folder="../../Results/Pending/"
done_results_folder="../../Results/Final/"
instances_folder="../../Instances/Pending/"
done_instances_folder="../../Instances/Final/"



if not os.path.exists(results_folder):
    print("check results_folder paths!")
    exit()

if not os.path.exists(instances_folder):
    print("check folder paths!")
    exit()




def process_log_file(log):

    for instance in log:
        filename = ""
        time = float("inf")
        time_limit = False
        objfunc = -1

        for k, v in instance.items():
            filename = k

            if not os.path.exists(os.path.join(instances_folder,filename)):
                continue

            if "time" in v:
                time = float(v["time"])
            else:
                continue

            if "ObjectiveFunction" in v:
                objfunc = int(v["ObjectiveFunction"])
            else:
                continue

            if "Solution" in v and "time limit exceeded" in v["Solution"]:
                time_limit = True

            # move instance file and rename
            instance_path = os.path.join(instances_folder,filename)

            time_str = str(int(time))
            l = len(time_str)
            trailing_zeroes = ""
            if l < 4:
                trailing_zeroes = "0" * (4 - l)
                

            filename2 = trailing_zeroes + time_str + "-" + filename
            if time_limit:
                filename2 = "timelimit-"+filename2
            new_path =  os.path.join(done_instances_folder, filename2)
            if os.path.exists(instance_path):
                shutil.move(instance_path, new_path)


def clean_json_file(logfile):

    processed = False

    with open(logfile,'r') as fin, open(logfile + ".temp",'w+') as fout:
        lines = fin.read()
        if not lines.endswith(']') and not lines.endswith("]\n"):
            processed = True
            print("processing "+logfile)
            # look for last ,
            iss = [match.start() for match in re.finditer(',', lines)]

            print("found commas")
            print(iss)
            print("")

            if len(iss) > 0:
                fixed = lines[:iss[-1]] + ',{"end":"end"}]'
                # then write {"end":"end"}] after that comma and discard the rest
                fout.write(fixed)

    if processed:
        shutil.move(logfile + '.temp', logfile)



os.chdir(results_folder)
print(os.getcwd())
for root, dirs, files in os.walk("."):
    all_ok = True
    for logfile in files:
        try:   
            logfilepath = os.path.join(root,logfile)
            if os.path.exists(logfilepath):

                clean_json_file(logfilepath)

                print("Processing " + logfilepath)
                log = json.load(open(logfilepath ))
                process_log_file(log)
        except Exception:
            all_ok = False
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
    
        # once finished move log file
        if all_ok:
            shutil.move(os.path.join(root,logfile), os.path.join(done_results_folder, logfile))            


