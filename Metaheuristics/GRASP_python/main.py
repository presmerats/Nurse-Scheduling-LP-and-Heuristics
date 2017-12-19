from Greedy import *
from LocalSearch import *
#from Grasp import *
#from BRKGA_main import *
from instance import *
import time

import sys
import os
import json
import cProfile

def greedyPlusLocalSearch(data):

    solution = GreedyConstructive(data)
    print(" GREEDY SOLUTION: ")
    pp.pprint(solution["cost"])
    print(time.time())
    print("")
    print("")



    failed_iterations = 0
    while failed_iterations < 3:

        solution2 = firstImprovementLocalSearch(solution, data)
        # solution2 = bestImprovementLocalSearch(solution, data)

        if solution2["cost"] >= solution["cost"]:
            print("     searching: " + str(solution2["cost"]))
            failed_iterations += 1
        else:
            print(" --> improvement: " + str(solution2["cost"]))
            failed_iterations = 0

        solution = solution2

    print(" LOCAL SEARCH SOLUTION: ")
    pp.pprint(solution["cost"])

    return solution


def grasp(data):
    pass

def brkga(data):
    pass


def readInstance(ipath):

    data = {}
    with open(ipath,'r') as f:
        for line in f.readlines():
            i1 = line.find("=")
            i2 = line.find(";")
            if line.startswith("maxConsec"):
                data["maxConsec"] = int(line[i1+1:i2])
            if line.startswith("maxPresence"):
                data["maxPresence"] = int(line[i1+1:i2])
            if line.startswith("maxHours"):
                data["maxHours"] = int(line[i1+1:i2])

            if line.startswith("minHours"):
                data["minHours"] = int(line[i1+1:i2])
            if line.startswith("hours"):
                data["hours"] = int(line[i1+1:i2])
            if line.startswith("nNurses"):
                data["nNurses"] = int(line[i1+1:i2])
            if line.startswith("demand"):
                j1 = line.find("[")
                j2 = line.find("]")
                liststr = line[j1+1:j2]
                demand = liststr.split(" ")
                data["demand"] = [ int(d) for d in demand if len(d)>0]

    return data 


def writeLog(instancepath, solver, solveTime , solution, data):

    results_list = []
    current_result = {}

    current_result[instancepath] = {}
    current_result[instancepath]["solver"] = solver
    current_result[instancepath]["time"] = str(round(solveTime,2)) 
    current_result[instancepath]["ObjectiveFunction"] = str(solution["cost"] )
    current_result[instancepath]["isMIP?"] = str(False) 
    current_result[instancepath]["data"] = data 
    current_result[instancepath]["solution"] = solution

    results_list.append(current_result)

    instance_name = os.path.basename(instancepath)
    instance_name = os.path.splitext(instance_name)[0] + '_' + solver + '.json'
    
    logpath = os.path.join('../../Results/Final/', instance_name)

    with open(logpath,'w+') as logfile:
        json.dump(results_list, logfile)


def run(instancepath, solverType):

    data = readInstance(instancepath)
    # pp.pprint(data)
    # exit()

    t1 = time.time()
    solution = None

    if solverType == "greedy":
        solution = greedyPlusLocalSearch(data)
    elif solverType == "grasp":
        solution = grasp(data)
    elif solverType == "brkga":
        solution = brkga(data)
    else:
        solverType = "greedy"
        #cProfile.run('greedyPlusLocalSearch(data)')
        solution = greedyPlusLocalSearch(data)

    t2 = time.time()
    solveTime = t2 - t1

    if solution is not None:
        writeLog(instancepath, solverType, solveTime, solution, data)


if __name__ == '__main__':

    data = {
        'maxConsec': maxConsec,
        'maxPresence': maxPresence,
        'maxHours': maxHours,
        'minHours': minHours,
        'hours': hours,
        'nNurses': nNurses,
        'demand': demand
    }

    instancepath = '../../Instances/Final/0001-i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-3Cnt-20171210_12-53-50687.dat'

    instancepath = '../../Instances/Final/0003-x_17_7.dat'
    # 12 s

    instancepath = '../../Instances/Final/0004-x_15_8.dat'
    # 7.1 s

    instancepath = '../../Instances/Final/0004-x_21_8.dat'
    # 154 s


    #instancepath = '../../Instances/Final/0005-i-ng-60-64-40-24h-10mxP-5mxC-10mxH-1mnH-3Cnt-20171218_23-50-01970.dat'

    #instancepath = '../../Instances/Final/0074-i-ng-60-64-40-24h-16mxP-5mxC-10mxH-2mnH-3Cnt-20171218_23-50-01921.dat'


    if len(sys.argv) > 1:

        solverType = sys.argv[1]

        if solverType not in ["greedy", "grasp", "brkga"]:
            print("Usage: python main.py <metaheuristic_algorithm>")
    else:
        solverType = "greedy"

    run(instancepath, solverType)

