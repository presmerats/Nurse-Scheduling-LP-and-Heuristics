from random import randrange
import time

from Greedy import *
from LocalSearch import *

def GraspConstructive(data, alpha_param=None):

    alpha = 0.5
    if alpha_param is not None:
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

        threshold = gcmin
        try:
            threshold = gcmin + alpha*(float(gcmax - gcmin))
        except:
            print(" gcmax " + str(gcmax) + " gcmin " + str(gcmin) + " threshold: " + str(threshold))

        i = 0
        for e in elements:
            if e.gc > threshold:
                break
            i += 1

        # improv 20180103
        #e = elements.pop(randrange(i))
        e = elements[0]

        # print("GRASP: selected element with cost " + str(e.gc) + " len: " + ",".join([ str(h) for h in  e.schedule]))
        solution = addElement(solution, e, data)

        #print(" last added " + str(solution["last_added"]) + " len(solution['w']" +str(len(solution['w']) ))

        if isFeasible(solution, data):
            break
        elif solution["last_added"] > len(solution["w"]) - 2:
            break


    print()
    print("After greedy loop finished -> Elements remaining=" + str(len(elements)) + " and isFeasible(solution)=" +  str(isFeasible(solution, data)) )

    solution["cost"], solution["totalw"] = computeCost(solution, data)
    print("Solution cost="+ str(solution["cost"]) )
    print(" pending:")
    print(solution["pending"])
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

    t1 = time.time()
    incumbent = GraspConstructive(data, 0)
    t2 = time.time()
    greedytime = t2 - t1
    print("|")
    print("-->greedyconstructive time: " + str(greedytime) )


    t3 = time.time()
    #solution = firstImprovementLocalSearch_mp(incumbent, data)
    solution = firstImprovementLocalSearch(incumbent, data)
    t4 = time.time()
    lstime = t4 - t3
    print("|")
    print("-->lstime: " + str(lstime) )
    print("")     


    if solution["cost"] < incumbent["cost"]:
        incumbent = solution
    
    while numiterations > 0:

        t1 = time.time()
        solution = GraspConstructive(data, alpha)
        t2 = time.time()
        greedytime = t2 - t1
        print("|")
        print("-->greedyconstructive time: " + str(greedytime) )

        t3 = time.time()
        solution2 = firstImprovementLocalSearch(solution, data)
        t4 = time.time()
        lstime = t4 - t3
        print("|")
        print("-->lstime: " + str(lstime) )
        print("")

        if solution2["cost"] < solution["cost"]:
            print("Quick LS -> Improvement: " + str(solution2["cost"]))
            solution = solution2

        if len(incumbent.keys()) == 0:
            incumbent = solution
        elif solution["cost"] < incumbent["cost"]:
            incumbent = solution

        numiterations -= 1

    print('Incumbent cost: ' + str(incumbent["cost"]))
    
    # Final intensive LS
    print('Intensive LS')
    # t5 = time.time()
    solution2 = []
    if ls == "first":
        solution2 = firstImprovementLocalSearch_intensive(incumbent, maxFailed, data)
    else:
        solution2 = bestImprovementLocalSearch_complex(incumbent, data)        
    incumbent = solution2
    # t6 = time.time()
    # flstime = t6 - t5 
    # print("|")
    # print("-->flstime: " + str(flstime) )
    # print("")

    print('Final solution')
    print(incumbent)
    print(incumbent["cost"])
    return incumbent