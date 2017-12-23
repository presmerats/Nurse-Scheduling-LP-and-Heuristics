import numpy as np
import sys, os
import pprint
import time
pp = pprint.PrettyPrinter(indent=2)

parentPath = os.path.abspath("../GRASP_python")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from LocalSearch2 import validCandidate
from Greedy import isFeasible


def checkIfCanWork(solution, h, n, data, sumW):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]

    w[n][h] = 1

    # minHours validity
    verify_minHours = False
    if z[n] == 1 and hours - h + 1 < minHours - sumW[n]:
        verify_minHours=True

    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = validCandidate(solution, data, n, verify_minHours=verify_minHours, whattoreturn='All')

    if rest_check and \
        maxPresence_check and \
        maxConsec_check and  \
        maxHours_check and \
        minHours_check:

        return True

    return False


def checkIfCanRest(solution, h, n, data, sumW, canWork_check):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]

    w[n][h] = 0

    # minHours validity
    verify_minHours = False
    if z[n] == 1 and hours - h + 1 < minHours - sumW[n]:
        verify_minHours=True

    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = validCandidate(solution, data, n, verify_minHours=verify_minHours, whattoreturn='All')

    if ((not rest_check and minHours_check) or \
        (not rest_check and not minHours_check) or \
        (rest_check and not minHours_check)) and \
       maxPresence_check and \
       maxConsec_check and  \
       maxHours_check :

        # cannot rest!, verify if can work:
        # should always be true at the same time!
        if not canWork_check:
            print(" INCOHERENCE DETECTED cannot rest but cannot work!")

        return canWork_check

    return False


def computeAssignments(solution, h, data, sumW, hini):
    """
        for each nurse,
            compute which nurses must work at time h to be valid
            compute which nurses can work at time h and still be valid
    """
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]

    mustWork = []
    canWork = []

    # for each nurse
    for n in range(data["nNurses"]):

        if h < hini[n]:
            continue

        # canWork Check-------------------------------
        canWork_check = checkIfCanWork(solution, h, n, data, sumW)
        if canWork_check:
           
            # mustWork Check-------------------------------
            # avoid repeating canWork_check
            mustWork_check = checkIfCanRest(solution, h, n, data, sumW, canWork_check)
            if mustWork_check:
                mustWork.append(n)
            else:
                canWork.append(n)
    
    return mustWork, canWork



def assignNurses(solution, hini, data):

    demand = data["demand"]
    pending = list(demand)
    hours = data["hours"]
    sumW = [0] * data["nNurses"]

    z = solution["z"]
    w = solution["w"]

    for h in range(hours):

        # for each hour

        # compute valid candidates
        #  those who must be assigned (rest constraint)
        #  those who can be assigned to work
        mustWork, canWork = computeAssignments(solution, h, data, sumW, hini)

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
        # print("")

        # for each nurse    
        #   try to assign if pending[h] > 0 and h >= hini[n]
        for n in mustWork:
            w[n][h] = 1
            sumW[n] += 1
            pending[h] -= 1
            if z[n] == 0:
                z[n] = 1
                solution["cost"] += 1

        if pending[h] > 0:
            for n in canWork:
                if h >= hini[n]:
                    w[n][h] = 1
                    sumW[n] += 1
                    pending[h] -= 1
                    if z[n] == 0:
                        z[n] = 1
                        solution["cost"] += 1
    
    # compute cost: already updated!

    # compute feasibility: if unfeasible -> fitness should be inf
    if not isFeasible(solution, data):
        # assign the max cost
        solution["cost"] = 2 * data["nNurses"]


def decode_hini(ind, data):

    start = data["hours"] + 1
    end = -1
    for i in range(len(data["demand"])):
        if data["demand"][i]  > 0:
            if i < start:
                start = i
            if i > end:
                end = i

    demandh_min = start
    demandh_max = end
    therange = demandh_max - demandh_min

    # print("demand start")
    # print(demandh_min)

    # print("demand end")
    # print(demandh_max)

    hini = []
    themin = demandh_max + 1
    themin_i = data["nNurses"] + 1
    themax = demandh_min -1 
    themax_i = -1
    for i in range(len(ind['chr'])):
        hi = int(therange * ind['chr'][i])
        # print(hi)
        # print(themin)
        # print(themax)
        if hi < themin:
            themin = hi
            themin_i = i
        if hi >= themax:
            # when all 3 are the same,
            # use >= in the max to avoid
            # pointing to the same index
            themax = hi
            themax_i = i
        hini.append(hi)

    # print(" hini min")
    # print(themin_i)
    # print(hini[themin_i])
    # print(demandh_min)
    # print(" hini max")
    # print(themax_i)
    # print(hini[themax_i])
    # print(demandh_max)
    #adjust min and max to real demand
    hini[themin_i] = demandh_min
    hini[themax_i] = demandh_max
    # print(" hini min")
    # print(themin_i)
    # print(hini[themin_i])

    # print(" hini min")
    # print(themin_i)
    # print(hini[themin_i])
    # print(demandh_min)
    # print(" hini max")
    # print(themax_i)
    # print(hini[themax_i])
    # print(demandh_max)

    if hini[themin_i] > start:
        # this happens if max and min are the same and in the same index!
        print(ind['chr'])
        print(hini)
        print("-->Error in min hini!")
        print("Min hini")
        print(hini[themin_i])
        print("start")
        print(start)
    # print(" hini max")
    # print(themax_i)
    # print(hini[themax_i])
    if hini[themax_i] < end:
        print(ind['chr'])
        print(hini)
        print("Error in max hini!")
        print("Max hini")
        print(hini[themax_i])
        print("en")
        print(end)
    # print("")
    # print("")
    # print("")

    return hini


def decode(population, data):
    """
        Idea 1)
            CHR = first work hour of the nurse

        Idea 2)
            CHR[i] = hi -> nursei start working at hi OR BEFORE

        Idea 3)
            CHR[i] = hi -> nursei start working at hi OR AFTER

    """

    for ind in population:

        # 1) transform from chr[i] to hini

        hours = data["hours"]
        # improvement1, use the first hour with demand, instead of 1...
        # improvement2, how to reduce infeasibility?

        hini = decode_hini(ind, data)

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

        # pp.pprint(data["demand"])
        # pp.pprint(solution)
        #time.sleep(5)

    return(population)