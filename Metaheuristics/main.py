import time
import sys
import os
import json
import cProfile


parentPath = os.path.abspath("./GRASP")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
parentPath = os.path.abspath("./BRKGA")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from Greedy import *
from LocalSearch import *
from Grasp import *
from BRKGA_main import *



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


def writeLog(instancepath,
             solver,
             solveTime,
             solution,
             data,
             results_path='../../Results/Final/',
             alpha=None,
             iterations=None,
             lstype=None,
             lsiterations=None,
             generations=None,
             eliteprop=None,
             mutantprop=None,
             population=None,
             inheritance=None):

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
    instance_name = os.path.splitext(instance_name)[0] + '-' + solver + '.json'
    
    if alpha and iterations and lstype:
        instance_name = os.path.splitext(instance_name)[0] \
            + '-' + solver \
            + '-a' + str(alpha) \
            + '-i' + str(iterations) \
            + '-lst' + str(lstype) \
            + '-lsit' + str(lsiterations) \
            + '.json'
        
    if generations and eliteprop and mutantprop and population and inheritance:
        instance_name = os.path.splitext(instance_name)[0] \
            + '-' + solver \
            + '-g' + str(generations) \
            + '-p' + str(population) \
            + '-e' + str(eliteprop) \
            + '-m' + str(mutantprop) \
            + '-i' + str(inheritance) \
            + '.json'

    logpath = os.path.join(results_path, instance_name)

    with open(logpath,'w+') as logfile:
        json.dump(results_list, logfile)
        print("written result to: " + logpath )


def run(instancepath, solverType,
        results_path=None,
        grasp_alpha=None,
        grasp_iterations=None,
        grasp_lstype=None,
        grasp_lsiterations=None,
        brkga_generations=None,
        brkga_eliteprop=None,
        brkga_mutantprop=None,
        brkga_population=None,
        brkga_inheritance=None
        ):

    # pass a set of params **kargvs
    # pass the results folder path

    data = readInstance(instancepath)
    # pp.pprint(data)
    # exit()

    t1 = time.time()
    solution = None

    if solverType == "greedy":
        solution = greedyPlusLocalSearch(data)
    elif solverType == "grasp":
        solution = grasp(data,
                         alpha=grasp_alpha,
                         iterations=grasp_iterations,
                         lstype=grasp_lstype,
                         lsiterations=grasp_lsiterations)
    elif solverType == "brkga":
        solution = brkga_run(data,
                             generations=brkga_generations,
                             eliteprop=brkga_eliteprop,
                             mutantprop=brkga_mutantprop,
                             population=brkga_population,
                             inheritance=brkga_inheritance)
    
    else:
        solverType = "greedy"
        solution = greedyPlusLocalSearch(data)

    t2 = time.time()
    solveTime = t2 - t1

    # final verification
    valid_feasible = isTotallyValid(data, solution)
    if valid_feasible:
        valid_feasible = isFeasible(solution, data)
    print("Valid and Feasible?: " + str(valid_feasible) )


    if solution is not None:
        try:
            if results_path:
                writeLog(instancepath=instancepath,
                         solver=solverType,
                         solveTime=solveTime,
                         solution=solution,
                         data=data,
                         results_path=results_path,
                         alpha=grasp_alpha,
                         iterations=grasp_iterations,
                         lstype=grasp_lstype,
                         lsiterations=grasp_lsiterations,
                         generations=brkga_generations,
                         eliteprop=brkga_eliteprop,
                         mutantprop=brkga_mutantprop,
                         population=brkga_population,
                         inheritance=brkga_inheritance)
            else:
                writeLog(instancepath=instancepath,
                         solver=solverType,
                         solveTime=solveTime,
                         solution=solution,
                         data=data,
                         alpha=grasp_alpha,
                         iterations=grasp_iterations,
                         lstype=grasp_lstype,
                         lsiterations=grasp_lsiterations,
                         generations=brkga_generations,
                         eliteprop=brkga_eliteprop,
                         mutantprop=brkga_mutantprop,
                         population=brkga_population,
                         inheritance=brkga_inheritance)    
        except Exception:
            print("Exception in user code:")
            print("-"*60)
            traceback.print_exc(file=sys.stdout)
            print("-"*60)
    else:
        print("solution is None!")


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


    #instancepath = '../Instances/Final/test_gc01.dat'

    instancepath = '../Instances/Final/test_gc02.dat'
    # gc+ls =  obj 2 t 0.02s
    # grasp :  obj 2 t 0.014s
    # brkga:  obj 2 t 35s(a=10,gen=2000) 7.4s(a=5,gen=1000)


    #instancepath = '../Instances/Final/test_gc03.dat'
    # 20171221  -firstImprovement obj=   - time= 


    #instancepath = '../Instances/Final/0000-x_8_1.dat'
    # 12 s
    # 20171221  -firstImprovement obj=7(greedy)   - time=759
    # 20171221  -bestsImprovement obj=7(greedy)   - time=675
    # 20171222  -firstImproement obj=7(greedy)   - time=0.6
    # 20171224  -brkga           obj=8           - time=271s


    #instancepath = '../Instances/Final/0004-x_15_8.dat'
    # 7.1 s

    instancepath = '../Instances/Final/0003-x_17_7.dat'
    # 12 s
    # 20171221 - of=16(greedy) - time = 173s
    # 20171221 - of=16(greedy) - time = 14s
    # 20171224 - of=14 (brkga) - tiem = 3182.9s

    #instancepath = '../Instances/Final/0004-x_21_8.dat'
    # 154 s
    # 20172222 - of=26(greedy) - t=57s

    #instancepath = '../Instances/Final/0001-i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-3Cnt-20171210_12-53-50687.dat'
    # 20171221 OBJ=40(g) time=665
    # 20171222 obj=40(g) t=6.5s

    #instancepath = '../Instances/Final/0001-i-ng-60-64-40-24h-8mxP-2mxC-2mxH-1mnH-3Cnt-20171210_12-53-51891.dat'
    # 20171222 obj=40(g) t=7.4s

    #instancepath = '../Instances/Final/0005-i-ng-60-64-40-24h-10mxP-5mxC-10mxH-1mnH-3Cnt-20171218_23-50-01970.dat'
    # 20171222 obj=47(ls) t=46s -> LS WORKS WELL!! greedy(59) vs ls(47)
    # 20171222 obj=47(ls) t=31s -> alph=0.2 ok, 0.5ok, 0.6 fails


    #instancepath = '../Instances/Final/0074-i-ng-60-64-40-24h-16mxP-5mxC-10mxH-2mnH-3Cnt-20171218_23-50-01921.dat'
    # 20171222 obj=57(greedy) t=317s
    # 20171222 obj=57(constr) t=421

    #instancepath = '../Instances/Final/1661-i-ng-60-128-80-24h-16mxP-5mxC-10mxH-1mnH-3Cnt-20171218_23-49-58683.dat'





    if len(sys.argv) > 1:

        solverType = sys.argv[1]

        if solverType not in ["greedy", "grasp", "brkga"]:
            print("Usage: python main.py <metaheuristic_algorithm>")
    else:
        solverType = "greedy"
        solverType = "grasp"
        solverType = "brkga"

    cProfile.run('run(instancepath, solverType)')   
    #run(instancepath, solverType)

