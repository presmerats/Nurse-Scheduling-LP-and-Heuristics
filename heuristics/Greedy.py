import math
import matplotlib.pyplot as pyplot
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=2)

class Element:
    def __init__(self, schedule):
        self.schedule = schedule
        self.gc = float("inf")

    def myprint(self):
        pp.pprint(self.schedule)
        pp.pprint(self.gc)
        print("")



def isValid(data, candidate):
    d = data

    validity = True

    maxHours_check = True
    sumW = 0
    maxConsec_check = True
    maxConsec_avoid = False
    consec = 0
    maxPresence_check = True
    start = -1
    end = -1
    rest_check = True
    rest_avoid = False
    rest = 0
    minHours_check = True
    minHours_avoid = False
    for w in range(len(candidate)):

        # maxHours
        sumW += candidate[w]
        maxHours_check = sumW <= d["maxHours"]

        # maxConsec
        #   -> just need to be checked on the last consec group of hours..
        if not maxConsec_avoid:
            if candidate[len(candidate) - w - 1] == 0:
                maxConsec_check = True
                maxConsec_avoid = True
            else:
                consec += 1
                if consec > d["maxConsec"]:
                    maxConsec_check = False
                    maxConsec_avoid = True
            
                maxConsec_check = consec <= d["maxConsec"]

                #print("maxconsec " + str(d["maxConsec"]) + " consec:" + str(consec))

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

        #print("maxPresence "+str(d["maxPresence"])+" start:"+str(start)+" end:"+str(end))

        # rest
        if not rest_avoid:
            if candidate[-1] == 1:
                rest_check = True

            else:
                if candidate[-2] == 1:
                    rest_check = True
                elif candidate[-2] == 0 and start < len(candidate) - 2 and end > len(candidate) - 2:
                    rest_check = False
                else:
                    rest_check = True
            rest_avoid = True

        # minHours (only if hours - minHours + 1 <= len(candidate))
        if w == len(candidate) - 1  and not minHours_avoid:
            if sumW < d["minHours"]  and d["hours"] - d["minHours"] + 1 <= len(candidate):
                #print("sumW: " + str(sumW) + " >= " + str(d["minHours"]) + "-" + str(d["hours"]) + "+" + str(len(candidate)) + " minHours_check: " + str(minHours_check))

                minHours_check = sumW >= d["minHours"] - (d["hours"] - len(candidate))
            minHours_avoid = True

        validity = minHours_check and \
            maxHours_check and \
            maxConsec_check and \
            maxPresence_check and \
            rest_check
        
        if not validity:
            break

    # print("validity: ")

    # print(candidate)
    # print(maxHours_check)
    # print(maxConsec_check)
    # print(maxPresence_check)
    # print(rest_check)
    # print(minHours_check)
    # print("=")
    # print(validity)
    return validity


# candidates construction
def buildCandidatesBaseCase():
    new_candidates= [[0], [1]]
    #print(new_candidates)
    return new_candidates


def buildCandidatesNormalCase(data, l):

    # call previous level
    if l==1:
        candidates = buildCandidatesBaseCase()
    else:
        candidates = buildCandidatesNormalCase(data, l-1)

    #print("buildCandidatesNormalCase "+str(l))

    # ini new set
    new_candidates = []


    # print(candidates)
    # print(type(candidates))
    # print(len(candidates))

    # create new candidates based on candidates
    for cand in candidates:

        # print(cand)
        # print(type(cand))
        # cand.append(0)
        # print(cand)

        # construct new cand.
        aux = list(cand)
        aux.append(0)
        if isValid(data, aux):
            new_candidates.append(aux)

        # construct new candi.
        aux = list(cand)
        aux.append(1)
        if isValid(data, aux):
            new_candidates.append(aux)

    #print(new_candidates)
    return new_candidates

def buildCandidates(data, l):

    # call previous level
    if l==1:
        candidates = buildCandidatesBaseCase()
    else:
        candidates = buildCandidatesNormalCase(data, l-1)


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


    candidates = buildCandidates(data, data["hours"])

    # duplicate those elements for each nurse?
    # or save a counter for each elements and when assigning it, subtract it
    for i in range(data["nNurses"]):
        for j in range(len(candidates)):
            elements.append(Element(list(candidates[j])))


    # print("----------------------------candidates: ")
    # pp.pprint([ e.schedule for e in elements])
    # print("")

    return elements



def update(solution, elements, data):
    """
        update the pending of the solution

    """
    w = solution["w"]
    
    print(solution["pending"])
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
    #print("----------------------------computing greedy cost:")


    for e in range(len(elements)):
        element = elements[e]
        partial_sum = 0
        for h in range(data["hours"]):
            dh = solution["pending"][h]
            partial_sum +=  dh * element.schedule[h]

        if partial_sum > 0:
            element.gc = 1.0 / partial_sum
        else:
            element.gc = float("inf")
            
        # print("")
        # element.myprint()



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
    cost = 0
    for h in range(len(solution["z"])):
        cost += solution["z"][h]

    return cost

def GreedyConstructive(data):

    # initialize solution and cost
    solution = {
        "cost": data["nNurses"],
        "w": [[0] * data["hours"]] * data["nNurses"],
        "z": [0] * data["nNurses"],
        "last_added": 0,
        "pending": [0] * data["hours"]
    }

    # initialize candidates
    elements = initializeCandidates(data)

    while len(elements) > 0:

        computeGreedyCost(solution, elements, data)

        elements = sorted(elements, key=lambda element: element.gc)

        e = elements.pop(0)
        solution = addElement(solution, e, data)
        if isFeasible(solution, data):
            break

        #update(solution, elements, data)


    print("after greedy loop finished: elements left=" + str(len(elements)) + " and isFeasible(soluion)" +  str(isFeasible(solution, data)) )
    solution["cost"] = computeCost(solution, data)
    return solution



