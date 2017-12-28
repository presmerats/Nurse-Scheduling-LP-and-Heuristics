import json
import sys
import os
import traceback
import shutil
import re



"""
    This script looks through all the Result json files for instances in the Instances/Final/MediumSet
    Then for each result for each instances in Instances/final/MediumSet it saves the json results into a separate file in Results/Final/MediumSet with the same name as the instance

"""





results_folder="../../../Results/Final/"
done_results_folder="./MediumSet"
instances_folder="../../Instances/Final/MediumSet"


if len(sys.argv)>1:
    os.chdir("../../Results/Final/MediumSet")
    for root, dirs, files in os.walk("."):
        for instance in files:
            try:
                if instance.endswith(".dat"):
                    shutil.move(os.path.join(root,instance),
                                os.path.join(root,instance[:-4] + "-ILP.json"))
            except Exception:
                
                print("Exception in user code:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)

    exit()






instances = []
realnameinstances = []


os.chdir(instances_folder)
for root, dirs, files in os.walk("."):
    for instance in files:
        try:
            i1 = instance.find("i-ng")
            name = instance[i1:]
            instances.append(name)
            realnameinstances.append(instance)

        except:
            pass


print(" medium set instances: ")
print(instances)
print(realnameinstances)
print("")
print("")


os.chdir(results_folder)
for root, dirs, files in os.walk("."):
    for thefile in files:
        if root.find('MediumSet') > -1:
            continue
        #print(os.path.join(root, thefile))

        try:
            results_list = json.load(open(os.path.join(root, thefile),'r') )
            for result in results_list:
                # get instance file name
                instance_name = os.path.basename(result.keys()[0])
                
                if instance_name == 'end':
                    continue
                #print(instance_name)
                if instance_name in instances:
                    print("found " + instance_name + " in instances")

                    new_list = []
                    new_list.append(result)

                    #get instance real name
                    real_name = instance_name
                    for rin in realnameinstances:
                        if rin.endswith(instance_name):
                            real_name = rin
                            break

                    final_result_file = os.path.join('./MediumSet',real_name)
                    json.dump(new_list, open(final_result_file,'w+'))

                elif instance_name in realnameinstances:
                    print("found " + instance_name + " in real name instances")
                    
                    new_list = []
                    new_list.append(result)

                    final_result_file = os.path.join('./MediumSet',instance_name)
                    json.dump(new_list, open(final_result_file,'w+'))



                # if instance name is in instances list 
                # or realname instances list 
                # then save to a new json list file 
                # in Results/Final/MediumSet

        except Exception:
            
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)