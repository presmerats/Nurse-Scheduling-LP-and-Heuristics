import numpy as np
import sys, os
import pprint
import time
from math import *
pp = pprint.PrettyPrinter(indent=2)


parentPath = os.path.abspath("../GRASP")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from Common.NurseSchedulingProblem import *
from Greedy import isFeasible


"""
    vars to save
        sumW
        consec
        start
        end

        checkers = []
        checker = {
            'sumW': 0,
            'consec': 0,
            'start': -1,
            'end': -1,
            'oldend': -1

        }


    checkIfCanWork

    checkIfMustWork


    complete_schedule_validation

    incremental_schedule_validation

    --change-to--

    complete_schedule_validation_fast
    incremental_schedule_validation_fast



"""

def computeAssignments(solution, h, data, sumW, checkers, hini=None):
    """
        for each nurse,
            if hini != None and h>hini[n] and z[n]==0 -> that nurse cannot work
            compute which nurses must work at time h to be valid
            compute which nurses can work at time h and still be valid

    """
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]

    mustWork = []
    canWork = []

    # sort nurses, first by those who work
    sorted_nurses = sorted(range(data["nNurses"]), key=lambda n: solution["z"][n], reverse=True)
    # print(solution["z"])
    # print(sorted_nurses)
    # print("")

    # for each nurse
    for n in sorted_nurses:

        # print()
        # print("computeAssignments " + str(n))

        # canWork Check-------------------------------
        canWork_check = checkIfCanWork_fast(solution, h, n, data, sumW, checkers=checkers, hini=hini)
        if canWork_check:
           
            # mustWork Check-------------------------------
            # avoid repeating canWork_check
            mustWork_check = checkIfMustWork_fast(solution, h, n, data, sumW, canWork_check, checkers,  hini)
            if mustWork_check:
                mustWork.append(n)
            else:
                canWork.append(n)

    return mustWork, canWork


def initCheckers(data):

    checkers = []

    for n in range(data["nNurses"]):
        checkers.append({
            'sumW': 0,
            'consec': 0,
            'start': -1,
            'end': -1
        } )
    
    return checkers


def assignNurses(solution, hini, data):

    """
        hini is used to add extra nurses at each hour
            hini[h]=0.2 -> means we add 0.1*demand[h] in terms of nurse assigments

    """

    demand = data["demand"]
    pending = solution["pending"]
    hours = data["hours"]
    sumW = [0] * data["nNurses"]


    checkers = initCheckers(data)

    z = solution["z"]
    w = solution["w"]

    for h in range(hours):

        #print(" for loop h="+str(h))
        
        mustWork, canWork = computeAssignments(solution, h, data, checkers=checkers, sumW=sumW )

        # print("h=" + str(h))
        # print("mustWork")
        # print(mustWork)
        # print("canWork")
        # print(canWork)
        # print("hini:")
        # print(hini)
        # print("demand")
        # print(data["demand"])
        # print("pending")
        # print(solution["pending"])


  
        #   try to assign if pending[h] > 0 and h >= hini[n]
        for n in mustWork:
            # print("nurse :" + str(n) + "  h: " + str(h) + " pending: ")
            # print(pending)
            w[n][h] = 1
            sumW[n] += 1
            pending[h] -= 1
            if z[n] == 0:
                z[n] = 1
                solution["cost"] += 1
            update_checkers(solution, data, n, h, 1,checkers)

            #print("w[" + str(n) + "," + str(h) + "] = 1")
            # pp.pprint(solution["w"])



        for n in canWork:
            # print("nurse :" + str(n) + "  h: " + str(h) + " pending: ")
            # print(pending)
            if pending[h] + hini[h] > 0:    
                w[n][h] = 1
                sumW[n] += 1
                pending[h] -= 1
                if z[n] == 0:
                    z[n] = 1
                    solution["cost"] += 1
                update_checkers(solution, data, n, h, 1,checkers)
                #print("w[" + str(n) + "," + str(h) + "] = 1")
            # print("w[" + str(n) + "]")
            # pp.pprint(solution["w"])

        # if h == 1 or h == 23:
        #     print("demand")
        #     print(data["demand"])
        #     print("pending")
        #     print(solution["pending"])
        #     pp.pprint(solution["w"])
        #     pp.pprint(checkers)

        
            

    # pp.pprint(data)
    # pp.pprint(solution["cost"])
    # exit()


    # compute feasibility: if unfeasible -> fitness should be inf
    if not isFeasible(solution, data):
        # assign the max cost
        solution["cost"] = 200000 * data["nNurses"]



def decode_hexcess(ind, data):
    hini = []

    for i in range(len(ind['chr'])):
        # option 2
        therange = data["demand"][i]
        # option 2b
        # therange = 10
        # option 2c
        # therange = 1
        # option 2d
        # therange = ceil(0.1*data["nNurses"])
        # option 2e
        # therange = ceil(0.3*data["nNurses"])

        #hi = int(therange * ind['chr'][i])
        
        # option 2f
        hi = 0
        if ind['chr'][i] < 0.2:
            therange = ceil(0.8 * data["nNurses"])
            hi = int(therange * ind['chr'][i])

        hini.append(hi)

    return hini


def diversity(population):

    s = set([x['fitness'] for x in population])
    return len(s)


def decode(population, data):
    """
        # diversify by excees of assignments per hour

    """

    for ind in population:

        hini = decode_hexcess(ind, data)
        
        # 2) assign work hours to nurses
        solution = {
            "cost": 0,
            "w": [[0] * data["hours"] for n in range(data["nNurses"])],
            "z": [0] * data["nNurses"],
            "last_added": 0,
            "pending": list(data["demand"]),
            "totalw": 0,
            "exceeding": [0] * data["hours"]
        }

        assignNurses(solution, hini, data)
        
        ind['solution'] = solution

        ind['fitness'] = solution["cost"]

    print("breed: " + str(len(population)) + " individuals")
    print("diversity: " + str(diversity(population)))
    return(population)


def getChrLength(data):
    return int(data["hours"])


