"""
    read files
        1) done_maxiter.txt & done_maxiter_bak2.txt or bak1
        2) intersect the list of files
        3) for each file -> find its results in (inside the json!!)
        4) copy the selected files to another folder

    repeat for done_alpha.txt


    repeat part 3,4 for done_generation.txt
        -> create list for the 7,12,17,22 generation values

"""
import json
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
from random import randrange
import re
import traceback
from datetime import datetime
import argparse
import operator
import shutil
import pprint

pp = pprint.PrettyPrinter(indent=2)




        


def extractParameterValue(parameter, filename):

    prefixes = {
        'alpha': {'prefix': '-a', 'type': 'float'},
        'maxiter': {'prefix': '-i', 'type': 'int'},
        'lsiteration': {'prefix': '-lsit', 'type': 'int'},
        'generation': {'prefix': '-g', 'type': 'int'},
        'population': {'prefix': '-p', 'type': 'int'},
        'inheritance': {'prefix': '-i', 'type': 'float'},
        'eliteprop': {'prefix': '-e', 'type': 'float'},
        'mutantprop': {'prefix': '-m', 'type': 'float'},
    }

    prefix = prefixes[parameter]["prefix"]
    i0 = filename.find('-i-ng')
    if i0 == -1:
        i0 = 0
    else:
        i0 += len('-i-ng')
    i1 = filename[i0:].find(prefix)
    i2 = i0 + i1 + len(prefix)
    i3 = filename[i2:].find('-')
    if i3 == -1:
        i3 = filename[i2:].find('.json')
    value = filename[i2:i2 + i3]

    if prefixes[parameter]["type"] == "float":
        try:
            value = float(value)
        except:
            print(parameter)
            print(prefix)
            print(i0)
            print(i1)
            print(i2)
            print(i2 + i3)
            print(filename)
            print(value)
            exit()
    else:
        value = int(value)

    return value



def parsefile(fileobject, parameters_list, parameter, filename):

    paramval = 0
    objfunc = 0

    # get param value from filename
    paramval = extractParameterValue(parameter, filename)


    if parameter == "generation" and not (paramval in [5,10 ,15 ,20 ]):
        return 



    # extract objective function
    results = json.load(fileobject)

    for elem in results:
        for k,v in elem.items():
            if k == 'end':
                continue
            # get objective function
            objfunc = int(v['ObjectiveFunction'])
            break

    
    # add new result to parameters_list
    for elem in parameters_list:
        if elem["name"] == parameter:
            param_results = elem["results"]
            
            found = False
            for res in param_results:
                if res["paramval"] == paramval:
                    found = True
                    res["objfunc"].append(objfunc)
                    l = len(res["objfunc"])
                    res["objfunc_avg"] = (res["objfunc_avg"] * (l - 1) + objfunc ) / l 
                    break

            if not found:
                param_results.append({
                    'paramval': paramval,
                    'objfunc': [objfunc],
                    'objfunc_avg': objfunc
                    })

            break


    return
    
   


if __name__ == '__main__':

    folder1 = os.path.join('..','..','Results','Final','LargeSet_20180106_bak','generation')
    folder2 = os.path.join('..','..','Results','Final','LargeSet_20180106_bak','To_merge_generations')


    # 1) readlines for done_maxiter.txt and done_maxiter_bak.txt
    maxiter_123 = []
    for root, dirs, files in os.walk(folder1):
        for result in files:
            maxiter_123.append(result)

    maxiter_678 = []
    for root, dirs, files in os.walk(folder2):
        for result in files:
            maxiter_678.append(result)


    # 2) cp files if they reference the same instance
    destination_folder = '../../Results/Final/LargeSet_20180106_bak/generation_merged3'
    os.makedirs(destination_folder)
    for filename in maxiter_678:
        i1 = filename.find('-brkga')
        if i1 == -1:
            continue

        name1 = filename[:i1]
        for filename2 in maxiter_123:
            if filename2.find('g10') > -1 or \
               filename2.find('g15') > -1 or \
               filename2.find('g20') > -1 or \
               filename2.find('g5') > -1:
               continue

            i2 = filename2.find('-brkga')
            if i2 == -1:
                continue

            name2 = filename2[:i2]
            if name1 == name2:
                #print("found coincidence!:" + filename + " with ")
                
                shutil.copy(
                        os.path.join(folder2,filename),
                        os.path.join(destination_folder,filename)
                        )
                shutil.copy(
                        os.path.join(folder1,filename2),
                        os.path.join(destination_folder,filename2)
                        )
   

    
