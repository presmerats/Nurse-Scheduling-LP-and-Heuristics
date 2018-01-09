# -*- coding: utf-8 -*-
"""
@author: Adrian Rodrigez Bazaga, Pau Rodriguez Esmerats
"""

import pprint
import os, sys
import time


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

                #print("-->valid elimination!  n" + str(n) + " h:" + str(h))
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


def find_reschedules(s, data):
    # find restschedules (for each h)  [nhh]
    restschedules = []
    sumW = [0] * data["nNurses"]
    for h in range(data["hours"]):
        restschedule = []

        # gather all fillable holes
        for n in range(data["nNurses"]):
            #print(s["w"][n])
            if s["z"][n] == 1 and s["w"][n][h] == 0:
                
                if h==-3:
                    print("h:" + str(h) + " n:" +str(n))
                    print(s["w"][n])
                # verify CanWork
                canwork = checkIfCanWork(s, h, n, data, sumW)
                if h==-3:
                    print(canwork)
                    print()

                # save the nurse num
                if canwork:
                    restschedule.append(n)

        # add to reschesdules
        restschedules.append(restschedule)


    return restschedules


def updateCost(s, data):

    for nz in range(data["nNurses"]):
        for hz in range(data["hours"]):
            if s["w"][nz][hz]==1:
                s["z"][nz]=1
                break
            if hz == 23:
                #print("empty nurse schedule " + str(nz))
                if s["w"][nz][hz]==1:
                    s["z"][nz]=1
                else: 
                    s["z"][nz]=0
        
    cost = 0
    for z in range(data["nNurses"]):
        cost += s["z"][z]

    s["cost"] = cost



def firstImprovementLocalSearch(solution, data, logger):
    # first improvement Local search: looks for new sols while improves

    # computes and stores the exceeding capacity
    exceedingNurseHours(solution, data)

    s = copySol(solution, data)

    # print("feasibility: " + str(isFeasible(s,data)))
    # print(data["demand"])
    # print(s["pending"])
    # print(s["cost"])
    # print()


    # remov all exceeding capacity [nh]
    for n in range(data["nNurses"]):
        exceedingCapacityRemoval(s, n, data)

    # updateCost(s, data)
    # print(s["z"])
    # print(s["cost"])
    # print()


    improved = True

    while improved:

        improved = False

        restschedules = find_reschedules(solution, data)
        # for sched in restschedules:
        #     print(sched)


        # select each complete restschedule and unassign a nurse that is not used in this restchedule
        # [nhn]


        # extract restschedule
        restschedule = extract_restschedule(restschedules)
        # print("extracted schedule")
        # print(restschedule)

        # how many emptiable nurses?
        for n in range(data["nNurses"]):

            if len(restschedules) < 1:
                continue
            
            # scan for non appearing but working nurse
            if n in restschedule:
              continue

            if s["z"][n] == 0:
                continue

            # exchange its working hours
            aux_schedule = list(s["w"][n])
            improving = False
            for h in range(data["hours"]):
                if s["w"][n][h] ==1 and restschedule[h] == -1:                    
                    improving = False
                    break
                elif s["w"][n][h]==1 and restschedule[h]>-1:
                    improving = True
                    s["w"][n][h] = 0
                    s["w"][restschedule[h]][h] = 1

            # final validation
            valid = True
            if improving:
                for nv in restschedule:
                    if nv > -1 :
                        valid = valid and complete_schedule_validation(s, data, nv, verify_minHours=True, whattoreturn='validity')
                        if not valid:
                            #print(" restschedule change verification:  " + str(nv) + " not valid final schedule")
                            break

            if improving and valid:

                # print(" --------------> nurse " + str(n) + " rescheduled!!!")
                # print("from :")
                # print(aux_schedule)
                # print("to :")
                # print(s["w"][n])

                # should be this without verification
                #s["z"] -= 1

                # print("extracted schedule")
                # print(restschedule)

                # cost = 0
                # for z in range(data["nNurses"]):
                #     cost += s["z"][z]

                # print("before computing new z")
                # print(s["z"])
                # print(" old cost: " + str(cost))
                # then compute and print again

                updateCost(s, data)
                if logger:
                    logger.update(s["cost"],0)

                # print("after computing new z")
                # print(s["z"])
                # print(" new cost: " + str(s["cost"]))

                # any non used hour of restschedule should be put back! to restschedules!
                # remove all assigned hours from restschedule
                for hz in range(data["hours"]):
                    if restschedule[hz]>-1 and  s["w"][restschedule[hz]][hz] == 0 :
                        restschedules[hz].append(restschedule[hz])
                        #print(" putting back " + str(restschedule[hz]))
                 
                # for sched in restschedules:
                #     print(sched)

                # clean the whiped nurse from restschedules
                clean_restschedules(restschedules, n)

                
                # extract new restschedule
                restschedule = extract_restschedule(restschedules)
                # print("extracted schedule")
                # print(restschedule)

            else:

                # if n == 0:


                # restore original schedule
                s["w"][n] = aux_schedule

                # print(" couldn't restchedule nurse  " + str(n))
                # print(s["w"][n])
                
                # found = False
                # for h in range(data["hours"]):
                #     if restschedule[h]>-1 and s["w"][restschedule[h]][h] == 1:
                #         print(" must undo " +str(restschedule[h]) + " at h:" + str(h))
                #         found = True
                # if found:      
                #     print(restschedule)
                #     for h in range(data["hours"]):
                #         if restschedule[h]>-1:
                #             print(s["w"][restschedule[h]][h])

                

                
                # remove all assigned hours from restschedule
                for h in range(data["hours"]):
                    if restschedule[h]>-1:
                        s["w"][restschedule[h]][h] = 0
                # if found:
                #     print("reassigning")

                #     for h in range(data["hours"]):
                #         if restschedule[h]>-1:
                #             print(s["w"][restschedule[h]][h])
      
                #     print()
                #     print()

        cost = 0
        for z in range(data["nNurses"]):
            cost += s["z"][z]

        s["cost"] = cost

        # verify that solution is feasible (shoulld not be necessary)
        if isFeasible(s,data):
            solution = s
        # else:
        #     print("feasibility: " + str(isFeasible(s,data)))
        #     print(data["demand"])
        #     print(s["pending"])

    return solution




def firstImprovementLocalSearch_intensive(incumbent, maxFailed, data, logger=None):

    failed_iterations = 0
    while failed_iterations < maxFailed:

        solution2 = firstImprovementLocalSearch(incumbent, data, logger)
        
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

