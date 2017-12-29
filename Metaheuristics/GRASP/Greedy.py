import math
import matplotlib.pyplot as pyplot
import numpy as np
import pprint
from copy import copy, deepcopy
import logging
import time
import os
import sys

from Common.Nurse import *

pp = pprint.PrettyPrinter(indent=2)

printlog = False


def create_logger(name):
    """
    Creates a logging object and returns it
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
 
    # create the logging file handler
    fh = logging.FileHandler('./greedy_logger.log')
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger

logger = create_logger("greedy")

def isValid_ng(data, candidate):
    d = data

    validity = True
    maxHours_check = True
    maxConsec_check = True
    maxPresence_check = True
    rest_check = True
    minHours_check = True
    
    maxHours_check = candidate.sumW <= d["maxHours"]
    maxConsec_check = candidate.consec <= d["maxConsec"]

    if candidate.end == -1 or candidate.start == -1:
        maxPresence_check = True  # should never happend!
    else:
        maxPresence_check = d["maxPresence"] >= candidate.end - candidate.start + 1




                  
    rest_check = ((candidate.rest == 0 and candidate.rest_1 == 0) or
                  (candidate.rest == 1 and candidate.rest_1 == 0) or 
                  (candidate.rest == 1 and candidate.rest_1 == 1 and
                    candidate.rest_2 == 0  ) or
                  (candidate.rest == 0 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == -1) or
                  (candidate.rest == 0 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 1 and candidate.start == len(candidate.schedule) ) or
                  (candidate.rest == 1 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 1 and candidate.start == -1 ) or
                  (candidate.rest == 1 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 1 and candidate.end < len(candidate.schedule) - 2 ) or
                  (candidate.rest == 1 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == -1 ) or
                  (candidate.rest == 0 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 0 ) 
                  )
                   



    minHours_check = True
    if candidate.sumW < d["minHours"]  and d["hours"] - d["minHours"] + 1 <= len(candidate.schedule):
        minHours_check = candidate.sumW >= d["minHours"] - (d["hours"] - len(candidate.schedule)) 


    validity = minHours_check and \
        maxHours_check and \
        maxConsec_check and \
        maxPresence_check and \
        rest_check
        
    # print("validity: ")
    # print(candidate.schedule)
    # print(candidate.start)
    # print(candidate.end)
    # print(candidate.sumW)
    # print(candidate.rest)
    # print(candidate.rest_1)
    # print(candidate.consec)
    # pp.pprint(data)

    # print(minHours_check)
    # print(maxHours_check)
    # print(maxConsec_check)
    # print(maxPresence_check)
    # print(rest_check)
    # print("=")
    # print(validity)

    return validity


def isValid(data, candidate):
    d = data

    validity = True

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

        # maxConsec
        #   -> just need to be checked on the last consec group of hours..
        
        maxConsec_check = False
        if candidate[-1] == 0 :
            maxConsec_check = True
        else:
            consec = 0
            for w in range(len(candidate)):

                
                if candidate[len(candidate) - w - 1] == 0:
                    maxConsec_check = True
                    break
                else:
                    consec += 1
                    if consec > d["maxConsec"]:
                        maxConsec_check = False
                        break
                
            
            maxConsec_check = consec <= d["maxConsec"]

            #print("maxconsec " + str(d["maxConsec"]) + " consec:" + str(consec))

        # maxPresence
        start = -1
        for w in range(len(candidate)):
            if candidate[w] == 1:
                start = w + 1
                break
        end = -1
        for w in range(len(candidate)):
            if candidate[len(candidate) - w - 1] == 1:
                end = len(candidate) - w
                break

        if end == -1 or start == -1:
            maxPresence_check = True  # should never happend!
        else:
            maxPresence_check = d["maxPresence"] >= end - start + 1

        #print("maxPresence "+str(d["maxPresence"])+" start:"+str(start)+" end:"+str(end))

        # rest
        if candidate[-1] == 1:
            rest_check = True
        else:
            if candidate[-2] == 1:
                rest_check = True
            elif candidate[-2] == 0 and start < len(candidate) - 2 and end > len(candidate) - 2:
                rest_check = False
            else:
                rest_check = True

        # minHours (only if hours - minHours + 1 <= len(candidate))
        minHours_check = True
        if sumW < d["minHours"]  and d["hours"] - d["minHours"] + 1 <= len(candidate):
            #print("sumW: " + str(sumW) + " >= " + str(d["minHours"]) + "-" + str(d["hours"]) + "+" + str(len(candidate)) + " minHours_check: " + str(minHours_check))

            minHours_check = sumW >= d["minHours"] - (d["hours"] - len(candidate))

        validity = minHours_check and \
            maxHours_check and \
            maxConsec_check and \
            maxPresence_check and \
            rest_check
        
        # print("validity: ")

        # print(candidate)
        # print(minHours_check)
        # print(maxHours_check)
        # print(maxConsec_check)
        # print(maxPresence_check)
        # print(rest_check)
        # print("=")
        # print(validity)
    return validity

def buildCandidates02_add(data, cand, value):

    newlist = cand.schedule
    newlist.append(value)
    newcand = Nurse(newlist, cand)

    if isValid_ng(data, newcand):
        return newcand

    return None

def buildCandidates02(data, l):


    candidates = []
    # call previous level
    for hini in range(data["hours"]):

        #print("-"*10 + "hini=" + str(hini))

        c1 = Nurse([0]*hini)
        c1.rest=1
        c1.sumW=0
        c1.start=-1
        c1.end=-1
        c1.consec=0
        c1.rest_1=-1
        c1.rest_2=-1

        c2 = Nurse([0]*hini)
        c2.rest=1
        c2.sumW=0
        c2.start=-1
        c2.end=-1
        c2.consec=0
        c2.rest_1=-1
        c2.rest_2=-1


        # c1.myprint()
        # c2.myprint()
        # pp.pprint(data)
        # print("-"*10)

        # first hour is schedule outside of the loop
        lastc2 = 0
        for h in range(hini+1,data["hours"] + 1):


            # first the continuous schedule
            #print("c1")
            if c1:
                new_c1 = buildCandidates02_add(data, c1, 1)
                if new_c1 is None:
                    c1.schedule = c1.schedule[:-1]
                    new_c1 = buildCandidates02_add(data, c1, 0)
                c1 = new_c1

            # then the sparse schedule
            #print("c2")
            if c2:
                if lastc2 == 0:
                    new_c2 = buildCandidates02_add(data, c2, 1)
                    lastc2 = 1
                    if new_c2 is None:
                        c2.schedule = c2.schedule[:-1]
                        new_c2 = buildCandidates02_add(data, c2, 0)
                        lastc2 = 0
                    c2 = new_c2

                else:
                    new_c2 = buildCandidates02_add(data, c2, 0)
                    lastc2 = 0
                    if new_c2 is None:
                        c2.schedule = c2.schedule[:-1]
                        new_c2 = buildCandidates02_add(data, c2, 1)
                        lastc2 = 1
                    c2 = new_c2

            if c1 is None and c2 is None:
                break

            # print("after the iteration: ")
            # if c1:
            #     c1.myprint()
            # if c2:
            #     c2.myprint()
            # print("-"*5)
            # print()

        

       

        if c1:
            #c1.myprint()
            candidates.append(c1)
        
        if c2:
            #c2.myprint()
            candidates.append(c2)

        
    # for c in candidates:
    #     c.myprint_short()

    return candidates


def initializeCandidates(data):
    """
        in:

            maxConsec = 6
            maxPresence = 14
            maxHours = 12
            minHours = 2
            hours = 24
            demand = [12, 20, 21, 17, 16, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            nNurses = 21

        out:
            elements=[
                 [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ...
                ]
        all possible schedules of a nurse, 
        taking into account the restriccions

    """

    elements = []

    # generate all possible candidates incrementally?
    # [0] or [1] -> check constraints at each stage (prune) except for minHours...
    # [0 0] or [0 1], [1 0], [1 1] -> recursive or dynamic programming?
    # recursive alg implemented in iterative structure?


    #candidates = buildCandidates(data, data["hours"])
    candidates = buildCandidates02(data, data["hours"])


    # duplicate those elements for each nurse?
    # or save a counter for each elements and when assigning it, subtract it
    for i in range(data["nNurses"]):
        elements.extend(deepcopy(candidates))


    # print("----------------------------candidates: ")
    # pp.pprint([ e.schedule for e in elements])
    # print("")

    return elements



def update(solution, elements, data):
    """
        update the pending of the solution

    """
    w = solution["w"]
    
    #print(solution["pending"])
    for h in range(len(solution["pending"])):
        sum_col=0
        for n in range(data["nNurses"]):
            sum_col += w[n][h]

        solution["pending"][h] = max(0, data["demand"][h] - sum_col)

    #print("updated: ")
    #print(solution["pending"])


def computeGreedyCost(solution, elements,  data):
    """
        for each element of the solution
            1/ SUM(1,hours)(demand[h] * w[n,h] )



    """
    if printlog:
        print("----------------------------computing greedy cost:")
        pp.pprint(data["demand"])
        pp.pprint(solution["pending"])
        pp.pprint(solution["w"])


    for e in range(len(elements)):
        element = elements[e]
        partial_sum = 0

        element.gc = data["nNurses"]
        
        for h in range(data["hours"]):
            pendingh = solution["pending"][h]
            element.gc -= element.schedule[h] * pendingh

        #     partial_sum +=  dh * element.schedule[h]

        # if partial_sum > 0:
        #     element.gc = 1.0 / partial_sum
        # else:
        #     element.gc = float("inf")
            
        # print("")
        #element.myprint()



def addElement(solution, e, data):

    """
        solution = {
            "cost": data["nNurses"],
            "w": [[0] * data["hours"]] * data["nNurses"],
            "z": [0] * data["nNurses"],
            "last_added": 0,
            "pending": [0] * data["hours"] 
        }
    """

    #pp.pprint(solution)

    z = solution["z"]
    w = solution["w"]
    i = solution["last_added"] + 1

    if i < len(w):
        w[i] = list(e.schedule)
        z[i] = 1
        solution["last_added"] += 1

        w = solution["w"]
    
    for h in range(len(solution["pending"])):
        sum_col=0
        for n in range(data["nNurses"]):
            sum_col += w[n][h]

        solution["pending"][h] = max(0, data["demand"][h] - sum_col)

    # print("----------------------------addElement: ")
    # pp.pprint(solution)

    return solution


def isFeasible(solution, data):
    """
        feasibility:
            - all demand is fulfilled
    """
    d = data["demand"]
    w = solution["w"]
    served = True
    for h in range(len(d)):

        sum_nurses = 0
        for n in range(len(w)):
            sum_nurses += w[n][h]

        if d[h] > sum_nurses:
            served = False
            break

        #print(" sum_ nurses "+ str(sum_nurses) + " h=" + str(h) + " pending: " + str(solution["pending"]) + " and demand " +  str(data["demand"]))

    #print(" sum_ nurses "+ str(sum_nurses) + " h=" + str(h) + " pending: " + str(solution["pending"]))

    return served




def computeCost(solution, data):
    """
        
    """

    # pp.pprint(data)
    # pp.pprint(solution)

    cost = 0
    totalw = 0
    for n in range(len(solution["z"])):
        cost += solution["z"][n]

        #print("nurse: " + str(n))
        for h in range(data["hours"]):

            # if printlog:
            #     print(" hours " + str(h))
            totalw += solution["w"][n][h]


    return cost, totalw

def GreedyConstructive(data):

    # initialize solution and cost
    solution = {
        "cost": data["nNurses"],
        "w": [[0] * data["hours"]] * data["nNurses"],
        "z": [0] * data["nNurses"],
        "last_added": -1,
        "pending": list(data["demand"])
    }

    # initialize candidates
    elements = initializeCandidates(data)
    # for e in elements:
    #     e.myprint_short()

    while len(elements) > 0:

        computeGreedyCost(solution, elements, data)


        # for e in elements:
        #     if e.schedule[0] == 1:
        #         e.myprint()
        # print("")

        elements = sorted(elements, key=lambda element: element.gc)


        # for e in elements[:5]:
        #     e.myprint()
        # print(len(elements))
        # print("")

        e = elements.pop(0)
        #e.myprint()
        solution = addElement(solution, e, data)


        if isFeasible(solution, data):
            break

        #update(solution, elements, data)


    pp.pprint(solution)
    pp.pprint(data)
    print()
    print("after greedy loop finished: elements left=" + str(len(elements)) + " and isFeasible(soluion)" +  str(isFeasible(solution, data)) )

    solution["cost"], solution["totalw"] = computeCost(solution, data)
    print("solution cost"+ str(solution["cost"]) )
    return solution




