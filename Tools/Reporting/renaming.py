import json
import sys
import os
import traceback
import shutil
import re



"""
This script is used to rename instances acording to their time to solve in ILP,  in order to have this naming schema

    0012-<instance name>.dat 

where 0012 means it took 12 seconds to solve the instance with ILP.

Basinc functionalities:
    moves inf-<instance>.dat to the Instances/Pending folder, in order for that instance to be solved again or the corresponding log record to be processed to save this instance with its proper name "timelimit-time-<instance>.dat"

    changes the names that begin with 12.0-<instance>.dat to 12-<instance>.dat 

    changes the names like 37-<instance>.dat to hvaing 4 trailing zeroes, 0037-<instance>.dat

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




os.chdir(done_instances_folder)
print(os.getcwd())
for root, dirs, files in os.walk("."):
    all_ok = True
    for instance in files:
        try:

            if instance.startswith("inf-"):
                

                instancepath = os.path.join(root,instance)
                print(instancepath)

                new_instance = instance[4:]
                new_instancepath = os.path.join(instances_folder,new_instance )

                print("--> "+new_instancepath)
                print("")

                shutil.move(instancepath, new_instancepath)

                # if os.path.exists(logfilepath):

                #     clean_json_file(logfilepath)

                #     print("Processing " + logfilepath)
                #     log = json.load(open(logfilepath ))
                #     process_log_file(log)

            i1 = instance.find(".0-i-ng")
            if i1 > 0 :
                
                instancepath = os.path.join(root, instance)

                instance2 = instance[:i1]+instance[i1+2:]

                instancepath2 = os.path.join(root, instance2)
                shutil.move(instancepath, instancepath2)
                print("found: " + instance)
                print("moved to :" +  instancepath2)
                print("")

            i2 = instance.find("-i-ng")
            if i2 > 0:
                time = instance[:i2]
                l = len(time)
                if l < 4:
                    trailing_zeroes = "0" * (4 - l)
                    instance2 = trailing_zeroes + instance
                    instancepath = os.path.join(root, instance)
                    instancepath2 = os.path.join(root, instance2)
                    shutil.move(instancepath, instancepath2)

            i3 = instance.find("-x_")
            if i3 > 0:
                time = instance[:i3]
                l = len(time)
                if l < 4:
                    trailing_zeroes = "0" * (4 - l)
                    instance2 = trailing_zeroes + instance
                    instancepath = os.path.join(root, instance)
                    instancepath2 = os.path.join(root, instance2)
                    shutil.move(instancepath, instancepath2)


        except Exception:
            all_ok = False
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
    
            


