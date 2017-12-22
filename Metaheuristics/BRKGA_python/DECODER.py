import numpy as np
import sys, os

parentPath = os.path.abspath("../GRASP_python")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from LocalSearch2 import validCandidate


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

    if rest_check2 and \
        maxPresence_check2 and \
        maxConsec_check2 and  \
        maxHours_check2 and \
        minHours_check2:

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


def computeAssignments(solution, h, data, sumW):
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
        mustWork, canWork = computeAssignments(solution, h, data, sumW)

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

        hini = [int(hours * ci) for ci in ind['chr']]



        # 2) assign work hours to nurses
        solution = {
            "cost": 0,
            "w": [],
            "z": [0] * data["nNurses"],
            "last_added": 0,
            "pending": [0] * data["hours"],
            "totalw": 0,
            "exceeding": [0] * data["hours"]
        }

        assignNurses(assignment, hini, data)

        ind['solution']=solution

        ind['fitness']=solution["cost"]

    return(population)