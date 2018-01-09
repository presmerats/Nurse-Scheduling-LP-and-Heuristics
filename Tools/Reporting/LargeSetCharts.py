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
import shutil
import pprint

pp = pprint.PrettyPrinter(indent=2)


def chartPlot(plotname, savefilename, x, y, axisnames, labels):

    fig, ax = plt.subplots()
    
    xs = range(len(y))
    x0 = xs[0]
    x1 = xs[-1]
    y1 = y[0]
    for ys in y:
        if ys < y1:
            y1 = ys
    ax.plot([x0, x1], [y1, y1], 'k-', c='r')
    
    plt.plot(range(len(y)),y, marker='.', color='b', ls='', label=labels[0])

    plt.xticks(range(len(x)),x)
    plt.xlabel(axisnames[0])
    plt.ylabel(axisnames[1])


    ax.legend(loc='upper right', fontsize='small')
    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()
    #plt.axis([0, len(results), 0, max(y)])
    plt.savefig(os.path.join('..','LargeSet_graphs',savefilename  + '.png'))
    plt.show()
    plt.close()

    # copy to Documentation folder
    savename2 = 'best-' + savefilename[18:]
    shutil.copy(os.path.join('..','LargeSet_graphs',savefilename  + '.png'), os.path.join('..','..','..','Documentation','img',savename2  + '.png'))


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

    best_values = {}

    for elem in parameters_list:
        print(elem["name"])
        if elem["name"] == "generation":
            pp.pprint(elem)

        elem["results"] = sorted(elem["results"], key=lambda k: k['paramval'])

        bestvalue = elem["results"][0]["paramval"]
        min_objfunc_avg = elem["results"][0]["objfunc_avg"]

        # if elem["name"] == "generation":
        #     pp.pprint(elem)

        for paramval in elem["results"]:
            #print(paramval["paramval"])
            #print(paramval["objfunc_avg"])
        
            #avg verification
            thesum = 0
            for objfs in paramval["objfunc"]:
                thesum += objfs

            theavg = thesum / len(paramval["objfunc"])
            if round(theavg,2) != round(paramval["objfunc_avg"],2):
                print("----->Avg error!")
                print(theavg)
                print(paramval["objfunc_avg"])
                print()

            if paramval["objfunc_avg"] < min_objfunc_avg:
                min_objfunc_avg = paramval["objfunc_avg"]
                bestvalue = paramval["paramval"]

        best_values[elem["name"]] = bestvalue

        # plotname
        # plotfilename
        # x
        x_ = [ x["paramval"] for x in elem["results"]]
        # y
        y_ = [ y["objfunc_avg"] for y in elem["results"]]
        # legend
        # axes

        thelabel = elem["name"]
        if elem["name"] == "lsiteration":
            thelabel = "failedIterations"
        elif elem["name"] == "maxIter":
            thelabel = "maxIterations"
        elif elem["name"] == "generation":
            thelabel = "generations"
        
        

        chartPlot(
            plotname=elem["name"], 
            savefilename=name + "-" + elem["name"], 
            x=x_, 
            y=y_, 
            axisnames=["Parameter values", "Average objective function"], 
            labels=[thelabel])

        
    
    print(best_values)
    with open(os.path.join('..','LargeSet_graphs','BestValues-') +  name, 'w+' ) as fout:
        fout.write(json.dumps(best_values))



        


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


    # if parameter == "generation" and not (paramval in [5,10 ,15 ,20 ]):
    #     return 



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

    results_folder = os.path.join('..','..','Results','Final','LargeSet_20180106')

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder",help="folder where to read results from")

    args = parser.parse_args()


    if args.folder:
        results_folder = os.path.join(args.folder,'data')

 

    os.chdir(results_folder)
    parameters_list = []
    for root, dirs, files in os.walk("."):
        
        for folder in dirs:
            print(folder)
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
    