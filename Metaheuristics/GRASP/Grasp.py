import math
import matplotlib.pyplot as pyplot
import numpy as np
import pprint
from copy import copy, deepcopy
from random import randrange
import time

from Greedy import *
from LocalSearch import *

def GraspConstructive(data, alpha_param=None):

    alpha = 0.5
    if alpha_param:
        alpha = alpha_param

    # initialize solution and cost
    solution = {
        "cost": data["nNurses"],
        "w": [[0] * data["hours"]] * data["nNurses"],
        "z": [0] * data["nNurses"],
        "last_added": -1,
        "pending": list(data["demand"])
    }

    elements = initializeCandidates(data)

    while len(elements) > 0:

        computeGreedyCost(solution, elements, data)

        elements = sorted(elements, key=lambda element: element.gc)


        gcmin = elements[0].gc
        gcmax = elements[-1].gc

        
        threshold = gcmin + alpha*(float(gcmax - gcmin))

        i = 0
        for e in elements:
            if e.gc > threshold:
                break
            i += 1

        e = elements.pop(randrange(i))

        #print("GRASP: selected element with cost " + str(e.gc) + " left: " + str(len(elements)))
        solution = addElement(solution, e, data)


        if isFeasible(solution, data):
            break

        #update(solution, elements, data)


    #pp.pprint(solution)
    #print(solution["w"])
    #print(solution["z"])
    #pp.pprint(data)
    print()
    print("after greedy loop finished: elements left=" + str(len(elements)) + " and isFeasible(soluion)" +  str(isFeasible(solution, data)) )

    solution["cost"], solution["totalw"] = computeCost(solution, data)
    print("solution cost"+ str(solution["cost"]) )
    return solution



def grasp(data, alpha=None, iterations=None, lstype=None):

    # params
    #  - first improve or best improvement
    #  - num iteartions
    #  - alpha 


    numiterations = 5
    if iterations:
        numiterations = iterations

    ls = "first"
    if lstype:
        ls = lstype

    solution = GraspConstructive(data, alpha)
    print(" GRASP CONSTRUCTIVE SOLUTION: ")
    pp.pprint(solution["cost"])
    print(time.time())
    print("")
    print("")

    failed_iterations = 0
    while failed_iterations < numiterations:

        solution2 = []
        if ls == "first":
            solution2 = firstImprovementLocalSearch(solution, data)
        else:
            solution2 = bestImprovementLocalSearch(solution, data)

        if solution2["cost"] >= solution["cost"]:
            print("     searching, cost" +
                  str(solution2["cost"]) +
                  " total_w:" +
                  str(solution2["totalw"]))
            failed_iterations += 1
        else:
            print(" --> improvement: " + str(solution2["cost"]))
            failed_iterations = 0

        solution = solution2

    print(" LOCAL SEARCH SOLUTION: ")
    #pp.pprint(solution["w"])
    #print(solution["z"])
    pp.pprint(solution["cost"])

    return solution

def greedyPlusLocalSearch(data):

    solution = GreedyConstructive(data)
    print(" GREEDY SOLUTION: ")
    pp.pprint(solution["cost"])
    print(time.time())
    print("")
    print("")

    failed_iterations = 0
    while failed_iterations < 5:

        solution2 = firstImprovementLocalSearch(solution, data)
        #solution2 = bestImprovementLocalSearch(solution, data)

        if solution2["cost"] >= solution["cost"]:
            print("     searching, cost" + str(solution2["cost"]) + " total_w:" + str(solution2["totalw"]))
            failed_iterations += 1
        else:
            print(" --> improvement: " + str(solution2["cost"]))
            failed_iterations = 0

        solution = solution2

    print(" LOCAL SEARCH SOLUTION: ")
    pp.pprint(solution["w"])
    print(solution["z"])
    pp.pprint(solution["cost"])

    return solution