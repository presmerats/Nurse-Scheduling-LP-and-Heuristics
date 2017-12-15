from Greedy import *
from LocalSearch import *
#from Grasp import *
#from BRKGA_main import *
from instance import *

import sys

def greedyPlusLocalSearch(data):

    solution = GreedyConstructive(data)
    print(" GREEDY SOLUTION: ")
    pp.pprint(solution)
    pp.pprint(solution["cost"])
    print("")
    print("")


    # testing local search
    # solution = { 'cost': 3,
    #     'last_added': 2,
    #     'pending': [0, 0, 0, 0],
    #     'w': [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    #     'z': [1, 1, 1]}
    # pp.pprint(solution)


    failed_iterations = 0
    while failed_iterations < 10:

        solution2 = firstImprovementLocalSearch(solution, data)
        # solution2 = bestImprovementLocalSearch(solution, data)

        if solution2["cost"] >= solution["cost"]:
            print("     searching: " + str(solution2["cost"]))
            failed_iterations += 1
        else:
            print(" --> improvement: " + str(solution2["cost"]))
            failed_iterations = 0

        solution = deepcopy(solution2)

    print(" LOCAL SEARCH SOLUTION: ")
    pp.pprint(solution)


def grasp(data):
    pass

def brkga(data):
    pass

if __name__ == '__main__':

    data = {
        'maxConsec': maxConsec,
        'maxPresence': maxPresence,
        'maxHours': maxHours,
        'minHours': minHours,
        'hours': hours,
        'nNurses': nNurses,
        'demand': demand
    }

    if len(sys.argv) > 1:

        if sys.argv[1] == "greedy":
            greedyPlusLocalSearch(data)
        elif sys.argv[1] == "grasp":
            grasp(data)
        elif sys.argv[1] == "brkga":
            brkga(data)
        else:
            print("Usage: python main.py <metaheuristic_algorithm>")

    else:
        greedyPlusLocalSearch(data)
