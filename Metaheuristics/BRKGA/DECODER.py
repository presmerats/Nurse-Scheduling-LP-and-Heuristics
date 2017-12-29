import numpy as np
import sys, os
import pprint
import time
pp = pprint.PrettyPrinter(indent=2)

parentPath = os.path.abspath("../GRASP")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from LocalSearch import validCandidate
from LocalSearch import incrementalValidCandidate
from Greedy import isFeasible


def checkIfCanWork(solution, h, n, data, sumW, hini=None):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]

    #print(z[n])
    #if z[n]==0:
    #    print("nurse " + str(n) + " check can work at " + str(h) + " cause hini =" + str(hini[n]) + " z[n]" + str(z[n]) + " can work?:"+ str(hini[n] < h and z[n]==0))
        
    if hini:
        if hini[n] < h and z[n]==0:
            #print("nurse " + str(n) + "cannot work at " + str(h) + " cause hini =" + str(hini[n]))
            return False

    aux = w[n][h]
    w[n][h] = 1

    # minHours validity
    verify_minHours = False
    if z[n] == 1 and hours - h + 1 < minHours - sumW[n]:
        verify_minHours=True

    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = validCandidate(solution, data, n, verify_minHours=verify_minHours, whattoreturn='All')

    # undo changes, just a verification
    w[n][h] = aux

    if rest_check and \
        maxPresence_check and \
        maxConsec_check and  \
        maxHours_check and \
        minHours_check:


        return True

    return False


def checkIfMustWork(solution, h, n, data, sumW, canWork_check, hini=None):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]
    aux = w[n][h]

    w[n][h] = 0

    # minHours validity
    verify_minHours = False
    if z[n] == 1 and hours - h + 1 < minHours - sumW[n]:
        verify_minHours = True

    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = incrementalValidCandidate(solution, data, n, verify_minHours=verify_minHours, whattoreturn='All', force_rest_check=False, set_end=h)

    # undo changes, just a verification
    w[n][h] = aux

    # print("CanRest w[" + str(n) + "][" + str(h) + "] = " + str(w[n][h]) + " ?:")
    # # print(rest_check)
    # print("rest_checkt " + str(rest_check))
    # print("minHours_checkt " + str(minHours_check))
    # print("maxHours_checkt " + str(maxHours_check))
    # print("maxConsec_checkt " + str(maxConsec_check))
    # print("maxPresence_checkt " + str(maxPresence_check))

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


def computeAssignments(solution, h, data, sumW, hini=None):
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


        # canWork Check-------------------------------
        canWork_check = checkIfCanWork(solution, h, n, data, sumW, hini)
        if canWork_check:
           
            # mustWork Check-------------------------------
            # avoid repeating canWork_check
            mustWork_check = checkIfMustWork(solution, h, n, data, sumW, canWork_check, hini)
            if mustWork_check:
                mustWork.append(n)
            else:
                canWork.append(n)


    return mustWork, canWork


def assignNurses(solution, hini, data):

    """
        hini is used as the highest hour at which a nuser can start working.
        If at hini a nuses has not started working, that nuser won't work.

        A nurse can work before hini,(if there is enough demand)
    """

    demand = data["demand"]
    pending = solution["pending"]
    hours = data["hours"]
    sumW = [0] * data["nNurses"]

    z = solution["z"]
    w = solution["w"]

    for h in range(hours):

        # for each hour

        # compute valid candidates
        #  those who must be assigned (rest constraint)
        #  those who can be assigned to work
        #  if h>hini and z[n]== 0 , that nurse cannot work
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
            #print("w[" + str(n) + "," + str(h) + "] = 1")
            # pp.pprint(solution["w"])



        for n in canWork:
            # print("nurse :" + str(n) + "  h: " + str(h) + " pending: ")
            # print(pending)
            if pending[h] > 0:    
                w[n][h] = 1
                sumW[n] += 1
                pending[h] -= 1
                if z[n] == 0:
                    z[n] = 1
                    solution["cost"] += 1
                #print("w[" + str(n) + "," + str(h) + "] = 1")
            # print("w[" + str(n) + "]")
            # pp.pprint(solution["w"])

        # if pending[h] > 0:
        #     print(" h:" + str(h) + " pending[h]=" + str(pending[h]))
        # print(solution["pending"])
        # print("")
        

    # pp.pprint(data)
    # pp.pprint(solution["cost"])
    # exit()

    # compute cost: already updated!

    # compute feasibility: if unfeasible -> fitness should be inf
    if not isFeasible(solution, data):
        # assign the max cost
        solution["cost"] = 200000 * data["nNurses"]


def decode_hini_simple(ind, data):

    hini = []
    therange = data["hours"]
    for i in range(len(ind['chr'])):
        hi = int(therange * ind['chr'][i])
        hini.append(hi)

    return hini





def assignNurses2(solution, hini, data):

    """
        hini is used to add extra nurses at each hour
            hini[h]=0.2 -> means we add 0.1*demand[h] in terms of nurse assigments

    """

    demand = data["demand"]
    pending = solution["pending"]
    hours = data["hours"]
    sumW = [0] * data["nNurses"]

    z = solution["z"]
    w = solution["w"]

    for h in range(hours):

        # for each hour

        # compute valid candidates
        #  those who must be assigned (rest constraint)
        #  those who can be assigned to work
        #  if h>hini and z[n]== 0 , that nurse cannot work
        mustWork, canWork = computeAssignments(solution, h, data, sumW)

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
                #print("w[" + str(n) + "," + str(h) + "] = 1")
            # print("w[" + str(n) + "]")
            # pp.pprint(solution["w"])

        # if pending[h] > 0:
        #     print(" h:" + str(h) + " pending[h]=" + str(pending[h]))
        # print(solution["pending"])
        # print("")
        

    # pp.pprint(data)
    # pp.pprint(solution["cost"])
    # exit()

    # compute cost: already updated!

    # compute feasibility: if unfeasible -> fitness should be inf
    if not isFeasible(solution, data):
        # assign the max cost
        solution["cost"] = 200000 * data["nNurses"]


def decode_hini_2(ind, data):
    hini = []
    
    for i in range(len(ind['chr'])):
        therange = data["demand"][i]
        hi = int(therange * ind['chr'][i])
        hini.append(hi)

    return hini




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

        #hini = decode_hini_simple(ind, data)
        hini = decode_hini_2(ind, data)

        # print("demand:")
        # print(data["demand"])
        # print("hini:")
        # print(hini)


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

        #assignNurses(solution, hini, data)
        assignNurses2(solution, hini, data)

        ind['solution'] = solution

        ind['fitness'] = solution["cost"]

		# print
        #pp.pprint(data["demand"])
        #pp.pprint(solution)
        #print(ind['fitness'])
        ##time.sleep(5)

    print("breed: " + str(len(population)) + " individuals")
    return(population)