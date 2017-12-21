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
        "totalw" : solution["totalw"]
    }

    
    return copied_sol

def nursesAtHourH( solution, h):

    sumN = 0
    for w in solution["w"]:
        sumN += w[h]
    return sumN




def electiveCandidates(solution, n, h, data):

    schedule = solution["w"][n]

    # get all other schedules
    candidates = []

    if data["demand"][h] < nursesAtHourH(solution,h):
        candidate = copySol(solution, data)
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



def findCandidates(solution, data, n):
    """ 
         this function returns solutions that include:
            - 0 hours assigned to nurse n
            - all the hours that where assigned to nurse n are assigned to other nurses 
            - the solution is feasible (valid constraints) and cover all demand

        strategies:
            1) find all possible combinations to satisfy this
            2) find the first combination to satisfy this

        not working...
            let a reduction of hours be a positive sign and return it
    """
    ns = [solution]
    # pp.pprint(ns)

    improved = False
    for h in range(data["hours"]):

        if printlog:
            print(" h = " + str(h))
            pp.pprint(solution["w"][n])

        partial_ns = []
        improved = False
        for s in ns:

            if solution["w"][n][h] == 1:

                # look for z, maxHours, maxPresence, maxConsec, (rest?)
                # not necessarily only z=1 candidates ...
                # (some diversity can be great)
                #   -> it depends on how many rounds the local search
                # runs, it should run one whole round
                # update each candidate
                # if no new candidates, return the current solution
                candidates = electiveCandidates(s, n, h, data)

                # add them to the set of new neighbors
                # new_ns.extend(candidates)
                if len(candidates) > 0:
                    partial_ns.extend(candidates)

        if len(partial_ns) > 0:
            improved = True
            # previous solution is no more considered
            ns = partial_ns

    # should return only those that have no working hours for nurse n
    if improved:
        return ns
    else:
        # return []
        # return ns as well
        return ns


def createNeighborhood(solution, data):

    Ns = []

    if printlog:
        print("Initial solutioni: " + "-"*24)
        pp.pprint(solution)
        print()


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

        if len(ns) > 0:
            Ns.extend(ns)

        
    return Ns 


def buildNewSol(neighbor):

    totalw = 0
    sumz = 0

    for n in range(len(neighbor["w"])):
            
        sumZn = 0
        for h in range(len(neighbor["w"][n])):
            totalw += neighbor["w"][n][h]
            sumZn += neighbor["w"][n][h]

        if sumZn > 0:
            neighbor["z"][n] = 1
            sumz += 1
        else:
            neighbor["z"][n] = 0

            

    neighbor["cost"] = sumz
    neighbor["totalw"] = totalw

    return neighbor



def firstImprovementLocalSearch(solution, data):

    Ns = createNeighborhood(solution, data)
    if printlog or printlog_mainloop:
        print()
        print("new neighborhood")
        pp.pprint(Ns)
    
    for i in range(len(Ns)):

        new_sol = buildNewSol( Ns[i])

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



def bestImprovementLocalSearch(solution, data):

    bestSolution = solution

    Ns = createNeighborhood(solution, data)
    if printlog or printlog_mainloop:
        print()
        print("new neighborhood")
        pp.pprint(Ns)

    for i in range(len(Ns)):

        new_sol = buildNewSol( Ns[i])

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

            if new_sol["cost"] < bestSolution["cost"]:

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) + " total_w:" + str(solution["totalw"]))

                bestSolution = new_sol

                
            elif (new_sol["cost"] == bestSolution["cost"] and
                new_sol["totalw"] < bestSolution["totalw"]):

                if printlog or printlog_mainloop:
                    print("-->IMPROVEMENT")
                    print("   " + str(new_sol["cost"]) + " total_w:" + str(solution["totalw"]))

                bestSolution = new_sol

                
            elif new_sol["cost"] >= bestSolution["cost"]:
                
                if printlog or printlog_mainloop:
                    print("same or worse cost" + str(new_sol["cost"]) + " vs " + str(bestSolution["cost"]))

                

    return bestSolution

