"""
    For each Results/Final/LargeSet_20180106/ subfolder:
        alpha
        maxiter
        lsiterations
        population
        eliteprop
        mutantprop
        generations
        inheritance

        create list of results
            ex: alpha_results = {
                'paramval': get from file,
                'objfunc': [],
                'objfunc_avg': value
            }
        for each file inside
            read and add data series
                alpha_results_x = "alpha param value"
                    -> get from file name
                alpha_results_y = objective function
                append alpha_results_y to objfunc

        compute average and save in objfunc_avg
        plot and save plot to Results/Final/LargeSet_20180106/Plots
        alpha_plot.png

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




def buildCharts(parameters_list, name):
    """
        parameters_list=[{
                'name': parameter,
                'results': [{
                    'paramval': paramval,
                    'objfunc': [objfunc],
                    'objfunc_avg': objfunc
                    },
                    {
                    'paramval': paramval,
                    'objfunc': [objfunc],
                    'objfunc_avg': objfunc
                    },
                    ...
                    ]
            },
            {
                'name': parameter,
                'results': [{
                    'paramval': paramval,
                    'objfunc': [objfunc],
                    'objfunc_avg': objfunc
                    },
                    {
                    'paramval': paramval,
                    'objfunc': [objfunc],
                    'objfunc_avg': objfunc
                    },
                    ...
                    ]
            },
            ]

        
    """

    for elem in parameters_list:
        print(elem["name"])
        elem["results"] = sorted(elem["results"], key=lambda k: k['paramval'])
        for paramval in elem["results"]:
            print(paramval["paramval"])
            print(paramval["objfunc_avg"])
        

    pass


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

    results_folder = '../../Results/Final/LargeSet_20180106'

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder",help="folder where to read results from")

    args = parser.parse_args()


    if args.folder:
        results_folder = os.path.join(args.folder,'data')

 

    os.chdir(results_folder)
    parameters_list = []
    for root, dirs, files in os.walk("."):
        
        for folder in dirs:
            # print(folder)
            parameter = folder
            parameter_results = {
                'name': parameter,
                'results': []
            }
            parameters_list.append(parameter_results)


        for result in files:
            parameter = root.split('/')[-1]

            if not result.endswith(".json"):
                continue

            filepath = os.path.join(root,result)
            with open(filepath,'r+') as f:
                try:
                    #print(os.path.join(root,result))
                    parsefile(f, parameters_list, parameter, result)
                    
                except Exception:
                    print()
                    print("Exception in " + result)
                    print("-"*60)
                    traceback.print_exc(file=sys.stdout)
                    print("-"*60)
        
    #print(parameters_list)
    buildCharts(parameters_list,  '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) )
    