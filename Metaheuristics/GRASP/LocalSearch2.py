# -*- coding: utf-8 -*-
"""
@author: Adrian Rodrigez Bazaga, Pau Rodriguez Esmerats
"""

import pprint
import os, sys


parentPath = os.path.abspath(".")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

pp = pprint.PrettyPrinter(indent=2)

from Greedy import *


printlog = False
printlog_mainloop = False
printlog_createNeighborhood = False
printlog_electiveCandidates = False
printlog_findCandidates = False
printlog_validity = False

def copySol(solution, data):

    copied_sol = {
        "cost": data["nNurses"],
        "w": deepcopy(solution["w"]),
        "z": list(solution["z"]),
        "last_added": 0,
        "pending": list(solution["pending"]),
        "totalw": solution["totalw"],
        "exceeding": list(solution["exceeding"])
    }

    return copied_sol


def exceedingCapacityRemoval(candidate, n, data):
    """
        Given a solution(candidate) and a nurse
        this function removes any assignment w[n][h] whenever
        capacity is exceeded at some hour h and
        the resulting schedule is valid
    """

    for h in range(data["hours"]):
        if candidate["w"][n][h] == 1 and candidate["exceeding"][h] > 0:
            candidate["w"][n][h] = 0

            # validate
            if complete_solution_validation(data, candidate):
                if printlog or printlog_electiveCandidates:
                    print("-->valid elimination!  n" + str(n) + " h:" + str(h))
                    pp.pprint(candidate)
                    print()

                candidate["exceeding"][h] -= 1
            else:
                candidate["w"][n][h] = 1


def buildNewSol(neighbor, data):
    """
        given a recently build solution (neighbor)
        this function computes:
            the cost,
            the exceeding capacity,
            the pending assignments
            the total assigned hours
    """

    totalw = 0
    sumz = 0
    columnarSum = [-1 * d for d in data["demand"]]
    columnarPending = list(data["demand"])

    for n in range(len(neighbor["w"])):

        sumZn = 0
        for h in range(len(neighbor["w"][n])):
            totalw += neighbor["w"][n][h]
            sumZn += neighbor["w"][n][h]
            # pending and exceeding
            columnarSum[h] += neighbor["w"][n][h]
            columnarPending[h] -= neighbor["w"][n][h]
            columnarPending[h] = max(columnarPending[h], 0)

        if sumZn > 0:
            neighbor["z"][n] = 1
            sumz += 1
        else:
            neighbor["z"][n] = 0

    neighbor["pending"] = columnarPending
    neighbor["exceeding"] = columnarSum
    neighbor["cost"] = sumz
    neighbor["totalw"] = totalw

    return neighbor


def electiveCandidate(candidate, n, h, data):

    # first try to remove candidate assign if exceeding capcity
    if candidate["exceeding"][h] > 0:
        candidate["w"][n][h] = 0

        # validate
        if complete_solution_validation(data, candidate):
            if printlog or \
               printlog_electiveCandidates or \
               printlog_findCandidates:
                print("-->valid elimination!  n" + str(n) + " h:" + str(h))
                pp.pprint(candidate)
                print()

            # update pending and exceeding
            candidate["exceeding"][h] -= 1

            return candidate
        else:
            # if this removing is not valid, restore state
            candidate["w"][n][h] = 1

    # then try to find a candidate replacement among other nurses
    for ni in (range(data["nNurses"])):

        # save state for nurse ni
        aux_list = list(candidate["w"][ni])
        aux_list2 = list(candidate["exceeding"])

        # remove all exceeding capacity assignmnts for nurse ni
        exceedingCapacityRemoval(candidate, ni, data)

        if ni == n:
            continue
        elif candidate["z"][ni] == 0:
            continue
        elif candidate["w"][ni][h] == 1:
            candidate["w"][ni] = aux_list
            continue
        else:

            if printlog or printlog_electiveCandidates:
                print("exchange " +
                      str(n) + ", " +
                      str(h) + " with " +
                      str(ni) + ", " +
                      str(h))

            candidate["w"][ni][h] = 1
            candidate["w"][n][h] = 0

            if complete_solution_validation(data, candidate):
                if printlog or printlog_electiveCandidates:
                    print("-->valid exchange!")
                    # pp.pprint(candidate)
                    print()

                return candidate

            else:
                # if exchange is not valid, restore state
                candidate["w"][ni] = aux_list
                candidate["w"][n][h] = 1
                candidate["exceeding"] = aux_list2

    # then try to place the hour assignment among nurses that do not work
    for ni in (range(data["nNurses"])):

        # save state for nurse ni
        aux_list = list(candidate["w"][ni])
        aux_list2 = list(candidate["exceeding"])

        # remove all exceeding capacity assignmnts for nurse ni
        exceedingCapacityRemoval(candidate, ni, data)

        if ni == n:
            continue
        elif candidate["z"][ni] == 1:
            continue
        else:

            if printlog or printlog_electiveCandidates:
                print("exchange " +
                      str(n) + ", " +
                      str(h) + " with " +
                      str(ni) + ", " +
                      str(h))

            candidate["w"][ni][h] = 1
            candidate["w"][n][h] = 0

            if complete_solution_validation(data, candidate):
                if printlog or printlog_electiveCandidates:
                    print("-->valid exchange!")
                    # pp.pprint(candidate)
                    print()

                return candidate

            else:
                # if exchange is not valid, restore state
                candidate["w"][ni] = aux_list
                candidate["w"][n][h] = 1
                candidate["exceeding"] = aux_list2

    return candidate


def findCandidate(solution, data, n):
    """ 
         this function returns a new solution that include:
            - 0 hours assigned to nurse n
            - all the hours that where assigned to nurse n
              are assigned to other nurses
            - the solution is valid (constraints)
    """

    # make changes to a copy s
    s = copySol(solution, data)
    for h in range(data["hours"]):

        if printlog or printlog_findCandidates:
            print(" h = " + str(h))
            pp.pprint(s["w"][n])

        if s["w"][n][h] == 1:
            electiveCandidate(s, n, h, data)

    s = buildNewSol(s, data)

    # pp.pprint(s)

    if s["z"][n]==0:
        # the nurse has been freed from work
        # the cost has decreased
        return [s]
    elif s["totalw"] < solution["totalw"]:
        # the cost has not decreased
        # but # assignments is reduced,
        # useful for further improvements
        return[s]
        #return[]
        
    else:
        
        return []


def nursesAtHourH(solution, h):
    """
        this function computes the total nurse assignments
        at hour h
    """
    sumN = 0
    for w in solution["w"]:
        sumN += w[h]
    return sumN


def exceedingNurseHours(solution, data):
    """
    this function computes and stores the
    exceeding capacity for each hour

    """

    solution["exceeding"] = [0] * len(solution["w"][0])
    for h in range(data["hours"]):
        solution["exceeding"][h] = nursesAtHourH(solution, h) - \
            data["demand"][h]

    if printlog or printlog_electiveCandidates:
        print("exceeding capacity")
        print(solution["exceeding"])
        print("")


def extract_restschedule(restschedules):

    result = []
    for restsched in restschedules:
        if len(restsched)>0:
            result.append(restsched.pop(0))
        else:
            result.append(-1)

    return result


def clean_restschedules(restschedules, n):

    for sched in restschedules:
        if n in sched:
            sched = sched.remove(n)

    return restschedules

def firstImprovementLocalSearch(solution, data):
    # first improvement Local search: looks for new sols while improves

    # computes and stores the exceeding capacity
    exceedingNurseHours(solution, data)

    s = copySol(solution, data)

    improved = True

    while improved:

        improved = False

        # remov all exceeding capacity [nh]
        for n in range(data["nNurses"]):
            exceedingCapacityRemoval(s, n, data)

        # find restschedules (for each h)  [nhh]
        #    -> when selecting a rest, verify CanWork() in this specific rest
        #    -> only add rests that are workable
        restschedules = []
        sumW = [0] * data["nNurses"]
        min_dimension = 0
        for h in range(data["hours"]):
            restschedule = []

            # gather all fillable holes
            for n in range(data["nNurses"]):
                #print(s["w"][n])
                if s["z"][n] == 1 and s["w"][n][h] == 0:
                    
                    # verify CanWork
                    canwork = checkIfCanWork(s, h, n, data, sumW)

                    # save the nurse num
                    if canwork:
                        restschedule.append(n)

            # add to reschesdules
            restschedules.append(restschedule)
            if len(restschedule) < min_dimension:
                min_dimension = len(restschedule)


        # for sched in restschedules:
        #     print(sched)


        # select each complete restschedule and unassign a nurse that is not used in this restchedule
        # [nhn]


        # extract restschedule
        restschedule = extract_restschedule(restschedules)


        # how many emptiable nurses?
        for n in range(data["nNurses"]):

            if len(restschedules) < 1:
                continue
            
            # scan for non appearing but working nurse
            if n in restschedule:
              continue

            if s["z"][n] == 0:
                continue

            # print("extracted schedule")
            # print(restschedule)


            # print("selected nurse before " + str(n))
            # print(s["w"][n])
            # print(" w before")
            # for nz in range(data["nNurses"]):
            #     print(s["w"][nz])
            # print()

            # exchange its working hours

            aux_schedule = list(s["w"][n])

            improving = True
            for h in range(data["hours"]):
                #print(" h " + str(h) + " wnh " + str(s["w"][n][h]) + " restschedule[h] " + str(restschedule[h]) )
                if s["w"][n][h] ==1 and restschedule[h] == -1:
                    
                    improving = False
                    break
                elif s["w"][n][h]==1 and restschedule[h]>-1:
                    improving = True
                    # print(" h " + str(h))
                    # print(restschedule)
                    # print( s["w"][restschedule[h]][h])
                    s["w"][n][h] = 0
                    s["w"][restschedule[h]][h] = 1


            # final validation
            valid = True
            for nv in restschedule:
                if nv > -1 :
                    valid = valid and complete_schedule_validation(s, data, nv, verify_minHours=True, whattoreturn='validity')
                    if not valid:
                        break


            # verify if valid -> no!
            # verfy if all -> no need!
            # recompute z[n]
            if improving and valid:
                # should be this without verification
                #s["z"] -= 1

                # print("extracted schedule")
                # print(restschedule)


                # print("before computing new z")
                # print(s["z"])
                # then compute and print again

                for nz in range(data["nNurses"]):
                    for hz in range(data["hours"]):
                        if s["w"][nz][hz]==1:
                            s["z"][nz]=1
                            break
                        if hz == 23:
                            #print("empty nurse schedule " + str(nz))
                            s["z"][nz]=0
                    
                # print("after computing new z")
                # print(s["z"])

                # any non used hour of restschedule should be put back! to restschedules!
                # remove all assigned hours from restschedule
                for hz in range(data["hours"]):
                    if restschedule[hz]>-1 and  s["w"][restschedule[hz]][hz] == 0 :
                        restschedules[hz].append(restschedule[hz])
                 
                # clean the whiped nurse from restschedules
                clean_restschedules(restschedules, n)

                # extract new restschedule
                restschedule = extract_restschedule(restschedules)

                # print("selected nurse after " + str(n))
                # print(s["w"][n])
                # # print(" w after")
                # # for n in range(data["nNurses"]):
                # #     print(s["w"][n])
                # print()
                # print()       

                

            else:
                # restore original schedule
                s["w"][n] = aux_schedule

                # remove all assigned hours from restschedule
                for h in range(data["hours"]):
                    if restschedule[h]>-1:
                        s["w"][restschedule[h]][h] = 0






        # verify that solution is feasible (shoulld not be necessary)
        #print("feasibility: " + str(isFeasible(s,data)))
        if isFeasible(s,data):
            solution = s

        cost = 0
        for z in range(data["nNurses"]):
            cost += solution["z"][z]

        print(" cost " + str(cost))
        solution["cost"] = cost
    
                    
    return solution




def firstImprovementLocalSearch_intensive(incumbent, maxFailed, data):

    failed_iterations = 0
    while failed_iterations < maxFailed:

        solution2 = firstImprovementLocalSearch(incumbent, data)
        
        if solution2["cost"] >= incumbent["cost"]:
            print("     Searching, Cost=" +
                  str(solution2["cost"]) +
                  " Total_W=" +
                  str(solution2["totalw"]))
            failed_iterations += 1
        else:
            print(" --> Improvement: " + str(solution2["cost"]))
            failed_iterations = 0

        incumbent = solution2

    return incumbent

