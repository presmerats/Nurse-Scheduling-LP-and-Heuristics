
import json
import sys
import os
import traceback


def newInstance(filelines, instance, output_folder, toreplace,replaceby,variable):
    instance2 = instance.replace(toreplace,replaceby)
    with open(os.path.join(output_folder,instance2),'w') as fout:
        for line in filelines:
            if line.startswith(variable):
                line = variable + " =" + str(replaceby) +";\n"
            fout.write(line)


instances_folder = '../../../Instances/Pending3/'
output_folder = '../../Instances/Final/ILPEvolution/data/'
os.chdir(instances_folder)
for root, dirs, files in os.walk("."):
    for instance in files:
        
        if not instance.startswith("0035"):
            continue

        filelines = []
        with open(os.path.join(root,instance),'r') as fin:
            filelines = fin.readlines()

        newInstance(filelines=filelines,
            instance=instance,
            output_folder=output_folder,
            toreplace='64',
            replaceby='128',
            variable='nNurses')
       
        newInstance(filelines=filelines,
            instance=instance,
            output_folder=output_folder,
            toreplace='64',
            replaceby='256',
            variable='nNurses')

        newInstance(filelines=filelines,
            instance=instance,
            output_folder=output_folder,
            toreplace='64',
            replaceby='512',
            variable='nNurses')

        newInstance(filelines=filelines,
            instance=instance,
            output_folder=output_folder,
            toreplace='64',
            replaceby='1024',
            variable='nNurses')