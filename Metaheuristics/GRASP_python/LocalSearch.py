import math
import matplotlib.pyplot as pyplot
import numpy as np
import pprint
from copy import copy, deepcopy

from Greedy import *

pp = pprint.PrettyPrinter(indent=2)

printlog = True


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

            if printlog:
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
            return validity

    return validity






def copySol(solution, data):

    copied_sol = {
        "cost": data["nNurses"],
        "w": deepcopy(solution["w"]),
        "z": list(solution["z"]),
        "last_added": 0,
        "pending": list(solution["pending"]),
    }

    
    return copied_sol



def electiveCandidates(solution, n, h, data):

    schedule = solution["w"][n]

    # get all other schedules
    candidates = []


    for ni in (range(data["nNurses"])):
        if ni == n:
            continue
        # elif solution["z"][ni] == 0:
        #     continue
        elif solution["w"][ni][h] ==1:
            continue
        else:

            #print("exchange " + str(n) + ", " + str(h) + " with " + str(ni) + ", " + str(h))
            # prepare the candidate (add the extra hour)
            
            candidate = copySol(solution, data)
            # print("copysol:"+"-"*24)
            # pp.pprint(solution)
            # pp.pprint(candidate)

            #pp.pprint(candidate)

            candidate["w"][ni][h] = 1
            candidate["z"][ni] = 1 # in case we use not working nurses also
            candidate["w"][n][h] = 0
            candidate["z"][n] = 0 # wait until the end to do this (or compute all vector to assure it can be set to 0) -> go that way

            if printlog:
                pp.pprint(candidate)

            # validate
            if isTotallyValid(data, candidate):
                if printlog:
                    print("-->valid!")
                    #pp.pprint(candidate)
                    print()
                    
                candidates.append(candidate)

    return candidates




def createNeighborhood(solution, data):

    Ns = []

    if printlog:
        print("Initial solutioni: " + "-"*24)
        pp.pprint(solution)
        print()


    for n in range(0, data["nNurses"] -1,1):
        if solution["z"][n] == 0:
            continue

        if printlog:
            print("")
            print("Nurse " + str(n))

        ns = [solution]
        #pp.pprint(ns)
        for h in range(data["hours"]):


            if printlog:
                print(" h = " + str(h) )
                pp.pprint(solution["w"][n])
            
            new_ns = []
            for s in ns:



                if solution["w"][n][h] == 1:

                    # look for z, maxHours, maxPresence, maxConsec, (rest?)
                    # not necessarily only z=1 candidates ... (some diversity can be great)
                    #   -> it depends on how many rounds the local search runs, it should run one whole round 
                    # update each candidate
                    # if no new candidates, return the current solution
                    candidates = electiveCandidates(s,n,h, data)

                    # add them to the set of new neighbors
                    #new_ns.extend(candidates)
                    if len(candidates)>0:
                        new_ns.extend(candidates)

            ns.extend(new_ns)


        if len(ns) > 1:
            Ns.extend(ns[1:])

        
    return Ns 


def buildNewSol(neighbor):

    sumz = 0
    for z in neighbor["z"]:
        sumz += z

    neighbor["cost"] = sumz 

    return neighbor



def firstImprovementLocalSearch(solution, data):

    update = True

    while update:
        update = False

        Ns = createNeighborhood(solution, data)
        if printlog:
            print()
            print("new neighborhood")
            pp.pprint(Ns)


        
        
        for i in range(len(Ns)):

            new_sol = buildNewSol( Ns[i])
            
            # print("new_sol")
            # pp.pprint(new_sol)
            # print()
            
            if not isFeasible(new_sol, data):
                if printlog:
                    print("unfeasible")
                continue
            else:
                #print("new solution: ")
                #pp.pprint(new_sol)
                #print(str(new_sol["cost"]))

                if new_sol["cost"] < solution["cost"]:

                    if printlog:
                        print("-->IMPROVEMENT")
                        print(str(new_sol["cost"]))

                    solution = new_sol
                    update = True
                    break
                elif new_sol["cost"] == solution["cost"]:
                    
                    if printlog:
                        print("same cost" + str(new_sol["cost"]))


            if update:
                break
                

    return solution


