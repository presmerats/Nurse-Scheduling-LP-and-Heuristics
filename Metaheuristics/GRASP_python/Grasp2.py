import math
import matplotlib.pyplot as pyplot
import numpy as np
import pprint
from copy import copy, deepcopy
from Greedy import *
from random import randrange


def GraspConstructive(data):

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

        alpha = 0.1
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



