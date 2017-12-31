import math
import matplotlib.pyplot as pyplot
import numpy as np
import pprint
from copy import copy, deepcopy
import os, sys

# parentPath = os.path.abspath("../../Metaheuristics/GRASP_python")
# if parentPath not in sys.path:
#     sys.path.insert(0, parentPath)
# parentPath = os.path.abspath("../GRASP_python")
# if parentPath not in sys.path:
#     sys.path.insert(0, parentPath)
# parentPath = os.path.abspath(".")
# if parentPath not in sys.path:
#     sys.path.insert(0, parentPath)

parentPath = os.path.abspath(".")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

pp = pprint.PrettyPrinter(indent=2)

#from Greedy import Greedy.isFeasible
from Greedy import *


printlog = False
printlog_mainloop = False
printlog_createNeighborhood = False
printlog_electiveCandidates = False
printlog_findCandidates = False
printlog_validity = False

def incrementalValidCandidate(candidate_sol, d, nurse, verify_minHours = True, whattoreturn = 'summary', force_rest_check = False, set_end=-1):

    candidate = candidate_sol["w"][nurse]

    maxHours_check = True
    sumW = 0
    maxConsec_check = True
    consec = 0
    maxPresence_check = True
    start = -1
    end = -1
    rest_check = True
    minHours_check = True

    stop = len(candidate)
    if set_end > -1:
        stop = set_end + 1

    for w in range(stop):

        # maxHours
        sumW += candidate[w]
        maxHours_check = sumW <= d["maxHours"]

        # maxConsec
        if candidate[stop - w - 1] == 0:
            consec = 0
        else:
            consec += 1
            if consec > d["maxConsec"]:
                maxConsec_check = False

        # maxPresence
        if start == -1:
            if candidate[w] == 1:
                start = w + 1
        #if end == -1:
        if candidate[w] == 1:
            end = w + 1
        # if candidate[stop - w - 1] == 1:
        #     end = stop - w

        if end != -1 and start != -1:
            maxPresence_check = d["maxPresence"] >= end - start + 1

        # print("           end "+str(end))
        # print("           start "+str(start))
        # print("           w[n]["+str(w)+"]="+str(candidate[w]))
        if end != -1 and start != -1 and w > start:
            if candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False
        elif force_rest_check:

            # rest
            # print(start)
            # print(end)
            # print(w)
            # try:
            #     print(candidate[w - 1])
            #     print(candidate[w])
            #     print(candidate[w - 1] == 1 or candidate[w - 1] == 0 and not candidate[w] == 0)
            # except:
            #     pass
            if w - 1 >= 0 and candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False

        # minHours (only if hours - minHours + 1 <= len(candidate))
        if sumW > 0 and verify_minHours:
            minHours_check = sumW >= d["minHours"]

    validity = minHours_check and \
        maxHours_check and \
        maxConsec_check and \
        maxPresence_check and \
        rest_check
    
    # print("validity: ")

    # print(candidate)
    # print(data)
    # print(minHours_check)
    # print(maxHours_check)
    # print(maxConsec_check)
    # print(maxPresence_check)
    # print(rest_check)
    # print("=")
    # print(validity)

    if not validity:

        if printlog or printlog_validity:
            print("validity: ")

            print(candidate)
            print(data)
            print("minHours: " + str(minHours_check))
            print("maxHours: " + str(maxHours_check))
            print("consec:   " + str(maxConsec_check))
            print("Presence: " + str(maxPresence_check))
            print("rest:     " + str(rest_check))
            print("=")
            print(validity)

    if whattoreturn == 'All':
        return (rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check )
    elif whattoreturn == 'rest':
        return rest_check
    elif whattoreturn == 'presence':
        return maxPresence_check
    elif whattoreturn == 'consec':
        return maxConsec_check
    elif whattoreturn == 'maxhours':
        return maxHours_check
    elif whattoreturn == 'minhours':
        return minHours_check

    return validity





def validCandidate(candidate_sol, d, nurse, verify_minHours = True, whattoreturn = 'summary', force_rest_check = False, set_end=-1):

    candidate = candidate_sol["w"][nurse]

    maxHours_check = True
    sumW = 0
    maxConsec_check = True
    consec = 0
    maxPresence_check = True
    start = -1
    end = -1
    rest_check = True
    minHours_check = True

    stop = len(candidate)
    if set_end > -1:
        stop = set_end + 1

    # look for end
    end = -1
    for h in range(len(candidate)):
        if candidate[h]==1:
            end = h

    #print(" end " + str(end))


    for w in range(stop):

        # maxHours
        sumW += candidate[w]
        maxHours_check = sumW <= d["maxHours"]

        # maxConsec
        if candidate[len(candidate) - w - 1] == 0:
            consec = 0
        else:
            consec += 1
            if consec > d["maxConsec"]:
                maxConsec_check = False

        # maxPresence
        if start == -1:
            if candidate[w] == 1:
                start = w + 1
        if end == -1:
            if candidate[len(candidate) - w - 1] == 1:
                end = len(candidate) - w
        if end != -1 and start != -1:
            maxPresence_check = d["maxPresence"] >= end - start + 1

        if end != -1 and start != -1 and w > start and w <= end:
            #print("validating rest_check")
            if candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False
                #print(candidate)
            #print(str(rest_check))
        elif force_rest_check:

            # rest
            # print(start)
            # print(end)
            # print(w)
            # try:
            #     print(candidate[w - 1])
            #     print(candidate[w])
            #     print(candidate[w - 1] == 1 or candidate[w - 1] == 0 and not candidate[w] == 0)
            # except:
            #     pass
            if w - 1 >= 0 and candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False

        # minHours (only if hours - minHours + 1 <= len(candidate))
        if sumW > 0 and verify_minHours:
            minHours_check = sumW >= d["minHours"]

    validity = minHours_check and \
        maxHours_check and \
        maxConsec_check and \
        maxPresence_check and \
        rest_check
    
    # print("validity: ")

    # print(candidate)
    # print(d)
    # print(minHours_check)
    # print(maxHours_check)
    # print(maxConsec_check)
    # print(maxPresence_check)
    # print(rest_check)
    # print("=")
    # print(validity)

    if not validity:

        if printlog or printlog_validity:
            print("validity: ")

            print(candidate)
            print(data)
            print("minHours: " + str(minHours_check))
            print("maxHours: " + str(maxHours_check))
            print("consec:   " + str(maxConsec_check))
            print("Presence: " + str(maxPresence_check))
            print("rest:     " + str(rest_check))
            print("=")
            print(validity)

    if whattoreturn == 'All':
        return (rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check )
    elif whattoreturn == 'rest':
        return rest_check
    elif whattoreturn == 'presence':
        return maxPresence_check
    elif whattoreturn == 'consec':
        return maxConsec_check
    elif whattoreturn == 'maxhours':
        return maxHours_check
    elif whattoreturn == 'minhours':
        return minHours_check

    return validity


def isTotallyValid(data, candidate):
    d = data

    candidate_sol = candidate

    validity = True

    for nurse in range(len(candidate_sol["w"])):
        validity = validCandidate(candidate_sol, d, nurse)
        if not validity:
            return False

    return validity


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
            if isTotallyValid(data, candidate):
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
        if isTotallyValid(data, candidate):
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

            if isTotallyValid(data, candidate):
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

            if isTotallyValid(data, candidate):
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


def createNeighborhood(solution, data):
    """
    creates a set of solutions that are
    neighbors to the current solution

    feasibility is not verified at this point
    (it should be feasible if input solution is feasible)
    """

    Ns = []

    if printlog:
        print("Initial solutioni: " + "-" * 24)
        pp.pprint(solution)
        print()

    # computes and stores the exceeding capacity
    exceedingNurseHours(solution, data)

    for n in range(0, data["nNurses"], 1):
        if solution["z"][n] == 0:
            continue

        if printlog or printlog_createNeighborhood:
            print("")
            print("Nurse " + str(n))

        ns = findCandidate(solution, data, n)

        if printlog or printlog_createNeighborhood:
            print(" after findCandidates " + "--" * 10)
            pp.pprint(ns)
            print("")

        if len(ns) > 0:
            Ns.extend(ns)

    return Ns


def createNeighborhood2(solution, data):
    """
    creates a set of solutions that are
    neighbors to the current solution

    feasibility is not verified at this point
    (it should be feasible if input solution is feasible)

    removes as many nurses as it cans in the same solution. 
    starting point matters here! 
    so calling function should randomize some how the nurse by which
    this function starts
    """

    Ns = []
    

    if printlog:
        print("Initial solutioni: " + "-" * 24)
        pp.pprint(solution)
        print()

    # computes and stores the exceeding capacity
    exceedingNurseHours(solution, data)

    nurse = 0
    while nurse < data["nNurses"]:
    #for nurse in range(0, data["nNurses"], 1):
        last_solution = solution
        zerofound = True

        #print(" point nurse " + str(nurse))
        last_nurse = 0
        for m in range(0, data["nNurses"], 1):
            last_nurse = m
            n = (m + nurse) % data["nNurses"]

            if solution["z"][n] == 0:
                continue

            #print(" internal nurse " + str(n))
            #print(" last_nurse " + str(m))

            new_solution = findCandidate(last_solution, data, n)

            if len(new_solution)>0:
                zerofound = False
                last_solution = new_solution[0]
                #print("found reassignment " + str(last_solution["cost"]))
                #if len(ns) > 0:
                # it saves all intermediate results
                # Ns.extend(last_solution)
                # or just return the one that contains all changes to assignments
                
            else:
                # when first non expendable nurse is found-> returns                
                #print("found impossible reassignment, quitting")

                # quick advancing, if no reassignment done still
                # then continue until first reassignment is done
                # only if reassignments have been done that it stops here
                if not zerofound:
                    break

        # if not the same sol as solution
        if not zerofound:
            #print("finally saving all new assignments")
            Ns.append(last_solution)

        # could be made advance quicker, like using last nurse reassigned + 1...
        if last_nurse == 0:
            nurse = nurse + 1
        else:
            nurse = nurse + last_nurse

    # print("----->finished at nurse "+ str(nurse))
    # for elem in Ns:
    #    print(elem["cost"])

    return Ns


def firstImprovementLocalSearch(solution, data):

    # 2 types of createNeighborhood2
    Ns = createNeighborhood(solution, data)
    if printlog or printlog_mainloop:
        print()
        print("new neighborhood")
        # pp.pprint(Ns)
    
    for i in range(len(Ns)):

        new_sol = Ns[i]

        if printlog or printlog_mainloop:
            print("new_sol")
            # pp.pprint(new_sol["z"])
            pp.pprint(new_sol["cost"])
            pp.pprint(new_sol["totalw"])
            print()

        if not isFeasible(new_sol, data):
            if printlog or printlog_mainloop:
                print("unfeasible")
            continue
        else:

            if new_sol["cost"] < solution["cost"]:

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) +
                          " total_w:" + str(solution["totalw"]))

                solution = new_sol
                return solution

            elif (new_sol["cost"] == solution["cost"] and
                  new_sol["totalw"] < solution["totalw"]):

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) +
                          " total_w:" + str(solution["totalw"]))

                solution = new_sol

            elif new_sol["cost"] == solution["cost"]:

                if printlog or printlog_mainloop:
                    print("same cost" + str(new_sol["cost"]))


    return solution


def bestImprovementLocalSearch(solution, data):

    Ns = createNeighborhood(solution, data)
    if printlog or printlog_mainloop:
        print()
        print("new neighborhood")
        pp.pprint(Ns)

    for i in range(len(Ns)):

        new_sol = Ns[i]

        if not isFeasible(new_sol, data):
            if printlog or printlog_mainloop:
                print("unfeasible")
            continue
        else:

            if new_sol["cost"] < solution["cost"]:

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) +
                          " total_w:" + str(solution["totalw"]))

                solution = new_sol

            elif (new_sol["cost"] == solution["cost"] and
                  new_sol["totalw"] < solution["totalw"]):

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) +
                          " total_w:" + str(solution["totalw"]))

                solution = new_sol

            elif new_sol["cost"] == solution["cost"]:

                if printlog or printlog_mainloop:
                    print("same cost" + str(new_sol["cost"]))

    return solution

