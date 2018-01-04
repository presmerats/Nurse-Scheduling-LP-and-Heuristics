
import json
import sys
import os
import traceback



instances_folder = '../../Instances'
os.chdir(instances_folder)
for root, dirs, files in os.walk("."):
    for instance in files:
        filelines = []
        with open(os.path.join(root,instance),'r') as fin:
            filelines = fin.readlines()

        with open(os.path.join(root,instance),'w') as fout:
            for line in filelines:
                if line.startswith("centroides"):
                    continue    
                fout.write(line)