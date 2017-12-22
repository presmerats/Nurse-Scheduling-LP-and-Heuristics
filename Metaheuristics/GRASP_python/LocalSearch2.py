import math
import matplotlib.pyplot as pyplot
import numpy as np
import pprint
from copy import copy, deepcopy

from Greedy import *

pp = pprint.PrettyPrinter(indent=2)

printlog = False
printlog_mainloop = False
printlog_createNeighborhood = False
printlog_electiveCandidates = False
printlog_findCandidates = False

def isTotallyValid(data, candidate):
    d = data

    candidate_sol = candidate

    validity = True

    for nurse in range(len(candidate_sol["w"])):
        
        candidate  = candidate_sol["w"][nurse]

        maxHours_check = True
        sumW = 0
        maxConsec_check = True
        consec = 0
        maxPresence_check = True
        start = -1
        end = -1
        rest_check = True
        rest = 0
        minHours_check = True
        for w in range(len(candidate)):

            # maxHours
            sumW += candidate[w]
            maxHours_check = sumW <= d["maxHours"]
            # if not maxHours_check:
            #     print("maxHours is not respected")
                
            # maxConsec 
            if candidate[len(candidate) - w - 1] == 0:
                consec = 0
            else:
                consec += 1
                if consec > d["maxConsec"]:
                    maxConsec_check = False
                    #print("maxconsec " + str(d["maxConsec"]) + " consec:" + str(consec) + " stop at "+str((len(candidate) - w)))
                  
            # maxPresence
            if start == -1:
                if candidate[w] == 1:
                    start = w + 1
                
            if end == -1: 
                if candidate[len(candidate) - w - 1] == 1:
                    end = len(candidate) - w
            
            if end != -1 and start != -1:
                maxPresence_check = d["maxPresence"] >= end - start + 1
                # if not maxPresence_check:
                #     print("maxPresence "+str(d["maxPresence"])+" start:"+str(start)+" end:"+str(end))
                    
            # rest
            if end != -1 and start != -1 and w > start and w <= end:
                if candidate[w - 1] == 0 and candidate[w] == 0:
                    rest_check = False
                    

            # minHours (only if hours - minHours + 1 <= len(candidate))
            
            # if sumW > 0 and sumW < d["minHours"] and d["hours"] - d["minHours"] + 1 <= len(candidate):
            #     #print("sumW: " + str(sumW) + " >= " + str(d["minHours"]) + "-" + str(d["hours"]) + "+" + str(len(candidate)) + " minHours_check: " + str(minHours_check))

            #     minHours_check = sumW >= d["minHours"] - (d["hours"] - len(candidate))

            if sumW > 0:
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

            # if printlog:
            #     print("validity: ")

            #     print(candidate)
            #     print(data)
            #     print("minHours: " + str(minHours_check))
            #     print("maxHours: " + str(maxHours_check))
            #     print("consec:   " + str(maxConsec_check))
            #     print("Presence: " + str(maxPresence_check))
            #     print("rest:     " + str(rest_check))
            #     print("=")
            #     print(validity)
            return validity

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


def exceedingCapacityRemoval(candidate,n,data):

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

    totalw = 0
    sumz = 0
    columnarSum = [-1*d for d in data["demand"]]
    columnarPending = list(data["demand"])

    for n in range(len(neighbor["w"])):
            
        sumZn = 0
        for h in range(len(neighbor["w"][n])):
            totalw += neighbor["w"][n][h]
            sumZn += neighbor["w"][n][h]
            # pending and exceeding
            columnarSum[h] += neighbor["w"][n][h]
            columnarPending[h] -= neighbor["w"][n][h]
            columnarPending[h] = max(columnarPending[h],0)


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


def electiveCandidates(solution, n, h, data):

    schedule = solution["w"][n]

    # get all other schedules
    candidates = []

    if solution["exceeding"] > 0:
        candidate["w"][n][h] = 0
        #candidate["z"][n] = 0

        # validate
        if isTotallyValid(data, candidate):
            if printlog or printlog_electiveCandidates:
                print("-->valid elimination!")
                pp.pprint(candidate)
                print()
                
            
            candidates.append(candidate)

            #return candidates

    for ni in (range(data["nNurses"])):
        if ni == n:
            continue
        # elif solution["z"][ni] == 0:
        #     continue
        elif solution["w"][ni][h] ==1:
            continue
        else:

            if printlog or printlog_electiveCandidates:
                print("exchange " + str(n) + ", " + str(h) + " with " + str(ni) + ", " + str(h))
            # prepare the candidate (add the extra hour)
            
            candidate = copySol(solution, data)
            # print("copysol:"+"-"*24)
            # pp.pprint(solution)
            # pp.pprint(candidate)

            # pp.pprint(candidate)

            candidate["w"][ni][h] = 1
            candidate["z"][ni] = 1 # in case we use not working nurses also
            candidate["w"][n][h] = 0
            #candidate["z"][n] = 0 # wait until the end to do this (or compute all vector to assure it can be set to 0) -> go that way

            # if printlog  or printlog_electiveCandidates:
            #     pp.pprint(candidate)

            # validate
            if isTotallyValid(data, candidate):
                if printlog or printlog_electiveCandidates:
                    print("-->valid exchange!")
                    #pp.pprint(candidate)
                    print()
      
                candidates.append(candidate)

    return candidates


def electiveCandidate(candidate, n, h, data):


    if candidate["exceeding"][h] > 0:
        candidate["w"][n][h] = 0

        # validate
        if isTotallyValid(data, candidate):
            if printlog or printlog_electiveCandidates or printlog_findCandidates:
                print("-->valid elimination!  n" + str(n) + " h:" + str(h))
                pp.pprint(candidate)
                print()

            # update pending and exceeding
            candidate["exceeding"][h] -= 1
            
            return candidate
        else:
            candidate["w"][n][h] = 1

    for ni in (range(data["nNurses"])):

        aux_list = list(candidate["w"][ni])
        aux_list2 = list(candidate["exceeding"])
        exceedingCapacityRemoval(candidate, ni, data)

        if ni == n:
            continue
        # elif solution["z"][ni] == 0:
        #     continue
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
                candidate["w"][ni] = aux_list
                candidate["w"][n][h] = 1
                candidate["exceeding"] = aux_list2

    return candidate


def findCandidates(solution, data, n):
    """ 
         this function returns solutions that include:
            - 0 hours assigned to nurse n
            - all the hours that where assigned to nurse n are assigned to other nurses 
            - the solution is feasible (valid constraints) and cover all demand
    """

    s = copySol(solution, data) 
       
    for h in range(data["hours"]):

        if printlog or printlog_findCandidates:
            print(" h = " + str(h))
            pp.pprint(s["w"][n])

        if s["w"][n][h] == 1:
            electiveCandidate(s, n, h, data)
        
    s = buildNewSol(s, data)

    #pp.pprint(s)

    if s["z"][n]==0:
        return [s]
    elif s["totalw"] < solution["totalw"]:
        #print("improved w! " + str(s["totalw"]))
        return[s]
    else:
        return []


def nursesAtHourH( solution, h):

    sumN = 0
    for w in solution["w"]:
        sumN += w[h]
    return sumN


def exceedingNurseHours(solution, data):

    solution["exceeding"] = [0]*len(solution["w"][0])
    for h in range(data["hours"]):
        solution["exceeding"][h]=nursesAtHourH(solution,h) - data["demand"][h]

    if printlog or printlog_electiveCandidates:
        print("exceeding capacity")
        print(solution["exceeding"])
        print("")



def createNeighborhood(solution, data):

    Ns = []

    if printlog:
        print("Initial solutioni: " + "-"*24)
        pp.pprint(solution)
        print()


    exceedingNurseHours(solution, data)

    for n in range(0, data["nNurses"],1):
        if solution["z"][n] == 0:
            continue

        if printlog  or printlog_createNeighborhood:
            print("")
            print("Nurse " + str(n))

        ns = findCandidates(solution, data, n )
        
        if printlog or printlog_createNeighborhood:
            print(" after findCandidates "+ "--"*10)
            pp.pprint(ns)
            print("")

        if len(ns)>0:
            Ns.extend(ns)

        
    return Ns






def firstImprovementLocalSearch(solution, data):

    Ns = createNeighborhood(solution, data)
    if printlog or printlog_mainloop:
        print()
        print("new neighborhood")
        #pp.pprint(Ns)
    
    for i in range(len(Ns)):

        new_sol = Ns[i]

        if printlog or printlog_mainloop:
            print("new_sol")
            #pp.pprint(new_sol["z"])
            pp.pprint(new_sol["cost"])
            pp.pprint(new_sol["totalw"])
            print()
        
        if not isFeasible(new_sol, data):
            if printlog or printlog_mainloop:
                print("unfeasible")
            continue
        else:
            #print("new solution: ")
            #pp.pprint(new_sol)
            #print(str(new_sol["cost"]))

            if new_sol["cost"] < solution["cost"]:

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) + " total_w:" + str(solution["totalw"]))

                solution = new_sol
                return solution

            elif (new_sol["cost"] == solution["cost"] and
                new_sol["totalw"] < solution["totalw"]):

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) + " total_w:" + str(solution["totalw"]))

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

        # print("new_sol")
        # pp.pprint(new_sol)
        # print()
        
        if not isFeasible(new_sol, data):
            if printlog or printlog_mainloop:
                print("unfeasible")
            continue
        else:
            #print("new solution: ")
            #pp.pprint(new_sol)
            #print(str(new_sol["cost"]))

            if new_sol["cost"] < solution["cost"]:

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) + " total_w:" + str(solution["totalw"]))

                solution = new_sol
                
            elif (new_sol["cost"] == solution["cost"] and
                new_sol["totalw"] < solution["totalw"]):

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) + " total_w:" + str(solution["totalw"]))

                solution = new_sol

            elif new_sol["cost"] == solution["cost"]:
                
                if printlog or printlog_mainloop:
                    print("same cost" + str(new_sol["cost"]))

    return solution

