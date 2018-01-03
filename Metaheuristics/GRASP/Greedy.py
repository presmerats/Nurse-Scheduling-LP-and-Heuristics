import pprint
import logging
from copy import copy, deepcopy
import multiprocessing as mp
import time
from random import random

from Common.Nurse import *
from Common.NurseSchedulingProblem import *

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

def buildCandidates_addHourAssignment(data, cand, value):

    newlist = cand.schedule
    newlist.append(value)
    newcand = Nurse(newlist, cand)

    if isValid_ng(data, newcand):
        return newcand

    return None

def buildCandidates(data):

    candidates = []
    # call previous level
    for hini in range(data["hours"]):
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

        c3 = Nurse([0]*hini)
        c3.rest=1
        c3.sumW=0
        c3.start=-1
        c3.end=-1
        c3.consec=0
        c3.rest_1=-1
        c3.rest_2=-1

        c4 = Nurse([0]*hini)
        c4.rest=1
        c4.sumW=0
        c4.start=-1
        c4.end=-1
        c4.consec=0
        c4.rest_1=-1
        c4.rest_2=-1

        c5 = Nurse([0]*hini)
        c5.rest=1
        c5.sumW=0
        c5.start=-1
        c5.end=-1
        c5.consec=0
        c5.rest_1=-1
        c5.rest_2=-1

        # first hour is schedule outside of the loop
        lastc2 = 0
        counter = 1
        
        for h in range(hini+1,data["hours"] + 1):


            # first the continuous schedule
            if c1:
                new_c1 = buildCandidates_addHourAssignment(data, c1, 1)
                if new_c1 is None:
                    c1.schedule = c1.schedule[:-1]
                    new_c1 = buildCandidates_addHourAssignment(data, c1, 0)
                c1 = new_c1

            # then the sparse schedule
            if c2:
                if lastc2 == 0:
                    new_c2 = buildCandidates_addHourAssignment(data, c2, 1)
                    lastc2 = 1
                    if new_c2 is None:
                        c2.schedule = c2.schedule[:-1]
                        new_c2 = buildCandidates_addHourAssignment(data, c2, 0)
                        lastc2 = 0
                    c2 = new_c2

                else:
                    new_c2 = buildCandidates_addHourAssignment(data, c2, 0)
                    lastc2 = 0
                    if new_c2 is None:
                        c2.schedule = c2.schedule[:-1]
                        new_c2 = buildCandidates_addHourAssignment(data, c2, 1)
                        lastc2 = 1
                    c2 = new_c2

            # then a randomized one
            if c3:
                #randc3 = random() > 0.3
                # now randc3 uses a modulo condition
                randc3 = counter % 5 != 0 
                if randc3:
                    new_c3 = buildCandidates_addHourAssignment(data, c3, 1)
                    #c3counter += 1
                    if new_c3 is None:
                        c3.schedule = c3.schedule[:-1]
                        new_c3 = buildCandidates_addHourAssignment(data, c3, 0)
                    
                    c3 = new_c3

                else:
                    new_c3 = buildCandidates_addHourAssignment(data, c3, 0)
                    
                    if new_c3 is None:
                        c3.schedule = c3.schedule[:-1]
                        new_c3 = buildCandidates_addHourAssignment(data, c3, 1)
                        #c3counter += 1
                    c3 = new_c3

                counter += 1

            # then a second randomized one
            if c4:
                # randc4 = random() <= 0.3
                # now randc3 uses a modulo condition
                randc4 = counter % 8 != 0 
                if randc4:
                    new_c4 = buildCandidates_addHourAssignment(data, c4, 1)
                    if new_c4 is None:
                        c4.schedule = c4.schedule[:-1]
                        new_c4 = buildCandidates_addHourAssignment(data, c4, 0)
                    c4 = new_c4

                else:
                    new_c4 = buildCandidates_addHourAssignment(data, c4, 0)
                    
                    if new_c4 is None:
                        c4.schedule = c4.schedule[:-1]
                        new_c4 = buildCandidates_addHourAssignment(data, c4, 1)
                        
                    c4 = new_c4

                counter += 1

            if c5:
                # randc4 = random() <= 0.3
                # now randc3 uses a modulo condition
                randc5 = counter % 4 != 0 
                if randc5:
                    new_c5 = buildCandidates_addHourAssignment(data, c5, 1)
                    if new_c5 is None:
                        c5.schedule = c5.schedule[:-1]
                        new_c5 = buildCandidates_addHourAssignment(data, c5, 0)
                    c5 = new_c5

                else:
                    new_c5 = buildCandidates_addHourAssignment(data, c5, 0)
                    
                    if new_c5 is None:
                        c5.schedule = c5.schedule[:-1]
                        new_c5 = buildCandidates_addHourAssignment(data, c5, 1)
                        
                    c5 = new_c5

                counter += 1

            if c1 is None and c2 is None and c3 is None and c4 is None and c5 is None:
                break

        if c1:
            candidates.append(c1)
        
        if c2:
            candidates.append(c2)

        if c3:
            candidates.append(c3)
            
        if c4:
            candidates.append(c4)
        
        if c5:
            candidates.append(c5)
        


    return candidates


def buildCandidates_mp(data, hini):

    candidates = []

    c1 = Nurse([0]*hini)
    c1.rest = 1
    c1.sumW = 0
    c1.start = -1
    c1.end = -1
    c1.consec = 0
    c1.rest_1 = -1
    c1.rest_2 = -1

    c2 = Nurse([0]*hini)
    c2.rest=1
    c2.sumW=0
    c2.start=-1
    c2.end=-1
    c2.consec=0
    c2.rest_1=-1
    c2.rest_2=-1

    # first hour is schedule outside of the loop
    lastc2 = 0
    for h in range(hini+1,data["hours"] + 1):


        # first the continuous schedule
        if c1:
            new_c1 = buildCandidates_addHourAssignment(data, c1, 1)
            if new_c1 is None:
                c1.schedule = c1.schedule[:-1]
                new_c1 = buildCandidates_addHourAssignment(data, c1, 0)
            c1 = new_c1

        # then the sparse schedule
        if c2:
            if lastc2 == 0:
                new_c2 = buildCandidates_addHourAssignment(data, c2, 1)
                lastc2 = 1
                if new_c2 is None:
                    c2.schedule = c2.schedule[:-1]
                    new_c2 = buildCandidates_addHourAssignment(data, c2, 0)
                    lastc2 = 0
                c2 = new_c2

            else:
                new_c2 = buildCandidates_addHourAssignment(data, c2, 0)
                lastc2 = 0
                if new_c2 is None:
                    c2.schedule = c2.schedule[:-1]
                    new_c2 = buildCandidates_addHourAssignment(data, c2, 1)
                    lastc2 = 1
                c2 = new_c2

        if c1 is None and c2 is None:
            break

    if c1:
        candidates.append(c1)
    
    if c2:
        candidates.append(c2)

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

    use_mp = False
    candidates = []

    if use_mp:
        cpus = mp.cpu_count() - 1
        pool = mp.Pool(processes=cpus)

        results = [pool.apply(buildCandidates_mp, args=(data,hini))
                      for hini in range(data["hours"])]

        # duplicate those elements for each nurse?
        # or save a counter for each elements and when assigning it, subtract it
        for i in range(data["nNurses"]):
            for p in results:
                for nurse in p:
                    elements.append(Nurse(nurse.schedule, nurse))


    else:
        candidates = buildCandidates(data)

        # duplicate those elements for each nurse?
        # or save a counter for each elements and when assigning it, subtract it
        # for i in range(data["nNurses"]):
        #     elements.extend(deepcopy(candidates))

        # this step is only needed before localsearch! but not here in greedy
        # copying schedules to avoid modifying one schedule modifies the others
        # if this is done later, then 
        # for i in range(data["nNurses"]):
        #     for nurse in candidates:
        #         elements.append(Nurse(nurse.schedule, nurse))

        #improvement 20180103
        for nurse in candidates:
            elements.append(Nurse(nurse.schedule, nurse))


    # print("----------------------------candidates: ")
    # pp.pprint([ e.schedule for e in elements])
    # print("")



    return elements



def update(solution, elements, data):
    """
        update the pending of the solution

    """
    w = solution["w"]
    
    for h in range(len(solution["pending"])):
        sum_col=0
        for n in range(data["nNurses"]):
            sum_col += w[n][h]

        solution["pending"][h] = max(0, data["demand"][h] - sum_col)


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


def addElement(solution, e, data):
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

    return solution

def computeCost(solution, data):
    cost = 0
    totalw = 0
    for n in range(len(solution["z"])):
        cost += solution["z"][n]

        for h in range(data["hours"]):
            totalw += solution["w"][n][h]


    return cost, totalw