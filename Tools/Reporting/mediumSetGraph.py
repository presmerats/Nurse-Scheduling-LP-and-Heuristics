
import json
import math
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
from random import randrange
import argparse
import traceback
from matplotlib.dates import date2num
import datetime



def nameExtraction(filename, solver):
    thename = filename

    if solver == "ILP":

        i1 = thename.find("-i")
        time_in_name = ""
        if i1>-1:
            time_in_name = thename[:i1]

        i2 = thename.find("-" + solver + ".json")
        i3 = thename.find("_")
        rand_name = ""
        if i2>-1 and i3>-1:
            rand_name = thename[i3+7:i2]

        instance_name = time_in_name + "-" + rand_name

        if instance_name == "-":
            thename=k
            i1 = k.find("-i")
            time_in_name = ""
            if i1>-1:
                time_in_name = k[:i1]

            i2 = k.find(".dat")
            i3 = k.find("_")
            rand_name = ""
            if i2>-1 and i3>-1:
                rand_name = k[i3+7:i2]

            instance_name = time_in_name + "-" + rand_name
    else:

        i1 = thename.find("-i")
        time_in_name = ""
        if i1>-1:
            time_in_name = thename[:i1]

        i2 = thename.find("-" + solver + "-" + solver)
        i3 = thename.find("_")
        rand_name = ""
        if i2>-1 and i3>-1:
            rand_name = thename[i3+7:i2]

        instance_name = time_in_name + "-" + rand_name

        if instance_name == "-":
            thename=k
            i1 = k.find("-i")
            time_in_name = ""
            if i1>-1:
                time_in_name = k[:i1]

            i2 = k.find(".dat")
            i3 = k.find("_")
            rand_name = ""
            if i2>-1 and i3>-1:
                rand_name = k[i3+7:i2]

            instance_name = time_in_name + "-" + rand_name

    # print("name extraction: " + thename)
    # print("short name: " + time_in_name + "-" + rand_name)
    return instance_name


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("folder",help="folder where to gather results from")
    args = parser.parse_args()


    # prepare 7 lists: 
    # ILP time, ILP objfunc, 
    # GRASP times, GRASP objfunc, 
    # BRKGA times BRKGA objfunc

    ILP_times = []
    ILP_objf = []
    ILP_instances = []
    
    GRASP_times = []
    GRASP_objf = []
    GRASP_instances = []

    BRKGA_times = []
    BRKGA_objf = []
    BRKGA_instances = []

    BRKGA_list = []
    GRASP_list = []
    ILP_list = []


    os.chdir(args.folder)
    for root, dirs, files in os.walk("."):
        results = []
        for filename in files:
            try:

                log = json.load(open(filename))
                #print(filename)
                for elem in log:

                    try:

                        for k,v in elem.items():
                            
                            if k == "end":
                                continue

                            # extract solver 
                            solver = "ILP"
                            if "solver" in v.keys():
                                solver = v["solver"]

                            # extract obj func
                            
                            if "ObjectiveFunction" in v.keys():
                                objf = int(v["ObjectiveFunction"])
                            else:
                                print(v.keys())
                                continue

                            # extract time
                            solvtime = float(v["time"])

                            # extract filename
                            # extract solving time from filename
                            # extract rand numbers from name at the end
                            # generate short name

                            instance_name = nameExtraction(filename, solver)

                            # save each to corresponding list
                            if solver == "ILP":
                                ILP_list.append(
                                    {"name": instance_name,
                                     "time": solvtime,
                                     "objf": objf})
                            elif solver == "grasp":
                                GRASP_list.append(
                                    {"name": instance_name,
                                     "time": solvtime,
                                     "objf": objf})
                            elif solver == "brkga":
                                BRKGA_list.append(
                                    {"name": instance_name,
                                     "time": solvtime,
                                     "objf": objf})

                            # if solver == "grasp":
                            #     print("processed elemet: "+thename+ " instance_name "+ instance_name)
                            #print("")

                    except Exception:
                        print("Exception in element:")
                        print("-"*60)
                        traceback.print_exc(file=sys.stdout)
                        print("-"*60)

                #print("processed file: "+filename)
                #print("")
            except:
                print("error in file : "+filename)
                print("")   
            
    # print(ILP_list)
    # print(GRASP_list)
    # print(BRKGA_list)
            

    # sort the 9 lists
    ILP_list= sorted(ILP_list, key=lambda k: int(k["name"][:4]) )
    GRASP_list = sorted(GRASP_list, key=lambda k: int(k["name"][:4]) )
    BRKGA_list = sorted(BRKGA_list, key=lambda k: int(k["name"][:4]) )


    for elem in BRKGA_list:
        if not elem["name"] in [ name['name'] for name in ILP_list]:
            print("not found BRKGA result instance " + elem["name"])
            continue

        BRKGA_instances.append(elem["name"])
        BRKGA_times.append(elem["time"])
        BRKGA_objf.append(elem["objf"])


    for elem in ILP_list:
        #this is temporary!!
        if elem["name"] not in [ elem['name'] for elem in BRKGA_list]:
            print("not found ILP result instance " + elem["name"])
            continue

        ILP_instances.append(elem["name"])
        ILP_times.append(elem["time"])
        ILP_objf.append(elem["objf"])



    for elem in GRASP_list:
        #this is temporary!!
        if elem["name"] not in [ elem['name'] for elem in ILP_list]:
            continue    
        GRASP_instances.append(elem["name"])
        GRASP_times.append(elem["time"])
        GRASP_objf.append(elem["objf"])


    # reduce to first 10


    # transform labels to 1 - 20
    NAMES_instances = []
    for i in range(len(BRKGA_instances)):
        NAMES_instances.append(i)


    # plot the times,

    fig, ax = plt.subplots() 
    ilp_line = plt.plot(range(len(ILP_instances)),ILP_times, marker='o', color='xkcd:goldenrod', ls='-', label='ILP')
    grasp_line = plt.plot(range(len(GRASP_instances)),GRASP_times, marker='+', color='xkcd:azure', ls='-', label='GRASP')
    brkga_line = plt.plot(range(len(BRKGA_instances)),BRKGA_times, marker='*', color='xkcd:grass green', ls='-', label='BRKGA')

    ax.legend(loc='upper left', fontsize='small')

    #plt.bar(range(len(y)),y, align='center')
    plt.xticks(range(len(NAMES_instances)),NAMES_instances)

    #plt.rc('xtick', labelsize=12)

    #plt.xticks(rotation='vertical')
    #plt.xticks(rotation=45, ha='right')

    plt.xlabel('instance name')
    plt.ylabel('Solve time(s)')

    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()

    fig1 = plt.gcf()
    fig1.savefig('../../../Documentation/img/ILPvsMetah_times.png')
    plt.show()
    plt.close()



     # plot the times for the first 10 results


    fig, ax = plt.subplots() 
    ilp_line = plt.plot(range(len(ILP_instances[:10])),ILP_times[:10], marker='o', color='xkcd:goldenrod', ls='-', label='ILP')
    grasp_line = plt.plot(range(len(GRASP_instances[:10])),GRASP_times[:10], marker='+', color='xkcd:azure', ls='-', label='GRASP')
    brkga_line = plt.plot(range(len(BRKGA_instances[:10])),BRKGA_times[:10], marker='*', color='xkcd:grass green', ls='-', label='BRKGA')

    ax.legend(loc='upper left', fontsize='small')

    #plt.bar(range(len(y)),y, align='center')
    plt.xticks(range(len(NAMES_instances[:10])),NAMES_instances[:10])

    #plt.xticks(rotation='vertical')
    #plt.xticks(rotation=45, ha='right')

    plt.xlabel('instance name')
    plt.ylabel('Solve time(s)')

    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()

    fig1 = plt.gcf()
    fig1.savefig('../../../Documentation/img/ILPvsMetah_times_first10.png')
    plt.show()
    plt.close()





    # plot the obj function values as lines
    fig, ax = plt.subplots() 
    ilp_line = plt.plot(range(len(ILP_instances)),ILP_objf, marker='o', color='xkcd:goldenrod', ls='-', label='ILP')
    grasp_line = plt.plot(range(len(GRASP_instances)),GRASP_objf, marker='+', color='xkcd:azure', ls='-', label='GRASP')
    brkga_line = plt.plot(range(len(BRKGA_instances)),BRKGA_objf, marker='*', color='xkcd:grass green', ls='-', label='BRKGA')

    ax.legend(loc='upper left', fontsize='small')


    #plt.bar(range(len(y)),y, align='center')
    plt.xticks(range(len(NAMES_instances)),NAMES_instances)

    #plt.xticks(rotation='vertical')
    #plt.xticks(rotation=45, ha='right')

    plt.xlabel('instance name')
    plt.ylabel('Objective Function')

    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()

    fig2 = plt.gcf()
    fig2.savefig('../../../Documentation/img/ILPvsMetah_objf.png')
    plt.close()
    plt.show()
    


    # plot the obj function values as histogram

    fig, ax = plt.subplots() 

    ax.bar([float(x) - 0.2 for x in range(len(ILP_objf))] , ILP_objf, width=0.2, color='xkcd:goldenrod', align='center', label='ILP' )
    ax.bar([float(x) for x in range(len(ILP_objf))], GRASP_objf, width=0.2, color='xkcd:azure', align='center', label='GRASP')
    ax.bar([float(x) + 0.2 for x in range(len(ILP_objf))], BRKGA_objf, width=0.2, color='xkcd:grass green', align='center', label='BRKGA')


    ax.legend( loc='upper left', fontsize='small')


    plt.xticks(range(len(NAMES_instances)),NAMES_instances)

    #plt.xticks(rotation='vertical')
    #plt.xticks(rotation=45, ha='right')

    plt.xlabel('instance name')
    plt.ylabel('Objective Function')

    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()

    fig1 = plt.gcf()
    fig1.savefig('../../../Documentation/img/ILPvsMetah_objf_hist.png')
    plt.show()
    plt.close()


    # plot the obj function values as histogram

    fig, ax = plt.subplots() 

    ax.bar([float(x) - 0.2 for x in range(len(ILP_objf[-10:]))] , ILP_objf[-10:], width=0.2, color='xkcd:goldenrod', align='center', label='ILP' )
    ax.bar([float(x) for x in range(len(ILP_objf[-10:]))], GRASP_objf[-10:], width=0.2, color='xkcd:azure', align='center', label='GRASP')
    ax.bar([float(x) + 0.2 for x in range(len(ILP_objf[-10:]))], BRKGA_objf[-10:], width=0.2, color='xkcd:grass green', align='center', label='BRKGA')


    ax.legend( loc='upper left', fontsize='small')


    plt.xticks(range(len(NAMES_instances[-10:])),NAMES_instances[-10:])

    #plt.xticks(rotation='vertical')
    #plt.xticks(rotation=45, ha='right')

    plt.xlabel('instance name')
    plt.ylabel('Objective Function')

    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()

    fig1 = plt.gcf()
    fig1.savefig('../../../Documentation/img/ILPvsMetah_objf_hist_last10.png')
    plt.show()
    plt.close()
