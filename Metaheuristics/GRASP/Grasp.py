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

    print()
    print("After greedy loop finished -> Elements remaining=" + str(len(elements)) + " and isFeasible(solution)=" +  str(isFeasible(solution, data)) )

    solution["cost"], solution["totalw"] = computeCost(solution, data)
    print("Solution cost="+ str(solution["cost"]) )

    return solution



def grasp(data, alpha=None, iterations=None, lstype=None, lsiterations=None):

    # params
    #  - first improve or best improvement
    #  - num iterations
    #  - alpha 


    numiterations = 5
    if iterations:
        numiterations = iterations

    maxFailed = 5
    if lsiterations:
        maxFailed = lsiterations

    ls = "first"
    if lstype:
        ls = lstype

    solution = []
    incumbent = {}
    
    while numiterations > 0:

        t1 = time.time()
        solution = GraspConstructive(data, alpha)
        t2 = time.time()
        greedytime = t2 - t1 
        print(" greedyconstructive time: " + str(greedytime) )
        print("")
        print("")
        

        t3 = time.time()
        solution2 = firstImprovementLocalSearch(solution, data)
        t4 = time.time()
        lstime = t4 - t3 
        print(" lstime: " + str(lstime) )
        print("")
        print("")

        if solution2["cost"] < solution["cost"]:
            print("Quick LS -> Improvement: " + str(solution2["cost"]))
            solution = solution2
            incumbent = solution2

        if len(incumbent.keys())==0:
            incumbent = solution


        numiterations -= 1

    print('Incumbent cost: ' + str(incumbent["cost"]))
    
    # Final intensive LS
    print('Intensive LS')
    failed_iterations = 0
    while failed_iterations < maxFailed:

        solution2 = []
        if ls == "first":
            solution2 = firstImprovementLocalSearch(incumbent, data)
        else:
            solution2 = bestImprovementLocalSearch(incumbent, data)

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
    #

    print('Final solution')
    print(incumbent)
    print(incumbent["cost"])
    return incumbent