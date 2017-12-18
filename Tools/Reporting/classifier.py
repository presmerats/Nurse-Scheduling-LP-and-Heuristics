import json
import sys
import os
import traceback
import shutil 



"""
 walk results folder
 for each log file
   load file to json, 
   for each instance
        get time
        get filename
        get if optimal or not
        move filename to done_instances_folder and rename
        move report json to done_results_folder 

"""

results_folder="../../Results/Pending/"
done_results_folder="../../Results/Final/"
instances_folder="../../Instances/Pending/"
done_instances_folder="../../Instances/Final/"


if not os.path.exists(results_folder) or os.path.exists(instances_folder):
    exit()




def process_log_file(log):

    for instance in log:
        filename = ""
        time = float("inf")
        time_limit = False
        objfunc = -1

        for k, v in instance.items():
            filename = k
            if "time" in v:
                time = float(v["time"])

            if "ObjectiveFunction" in v:
                objfunc = int(v["ObjectiveFunction"])

            if "Solution" in v and "time limit exceeded" in v["Solution"]:
                time_limit = True

            # move instance file and rename
            instance_path = os.path.join(instances_folder,filename)
            filename2 = str(rount(time,0)) + "-" + filename
            new_path =  os.path.join(done_instances_folder, filename2)
            if os.path.exists(instance_path):
                shutil.move(instance_path, new_path)




os.chdir(results_folder)
for root, dirs, files in os.walk("."):
    for logfile in files:
        try:
            log = json.load(open(logfile))
            process_log_file(log)
        except Exception:
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
    
    # once finished move log file
    shutil.move(os.path.join(root,logfile), os.path.join(done_results_folder, logfile))            


