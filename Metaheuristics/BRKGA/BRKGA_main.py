# imports
import math
import matplotlib.pyplot as plt
import pprint
import time
pp = pprint.PrettyPrinter(indent=2)

import BRKGA as brkga
# import DECODER_hexcess as decoder
# import DECODER_hini as decoder
# import DECODER_horder as decoder
# import DECODER as decoder
from CONFIGURATION import config


def brkga_run(data,
              generations=None,
              eliteprop=None,
              mutantprop=None,
              population=None,
              inheritance=None,
              decoder="hexcess"):

    # params
    #   - num generations
    #   - population size
    #   - inheritance probability
    #   - proportino of elite
    #   - proportion of mutants



    if decoder == "hexcess":
        import DECODER_hexcess_2 as decoder
    elif decoder == "hini":
        import DECODER_hini as decoder
    else:
        import DECODER_hexcess_2 as decoder
        # import DECODER_horder as decoder
    

    # initializations

    # must be derived from instance
    chrLength = decoder.getChrLength(data)

    numIndividuals = int(config['a']) * int(data["nNurses"])
    if population:
        numIndividuals = population * int(data["nNurses"])

    numElite = int(math.ceil(numIndividuals * config['eliteProp']))
    if eliteprop:
        numElite = int(math.ceil(numIndividuals * eliteprop))

    numMutants = int(math.ceil(numIndividuals * config['mutantProp']))
    if mutantprop:
        numMutants = int(math.ceil(numIndividuals * mutantprop))

    maxNumGen = int(config['maxNumGen'])
    if generations:
        maxNumGen = generations

    ro = float(config['inheritanceProb'])
    if inheritance:
        ro = inheritance

    numCrossover = max(numIndividuals - numElite - numMutants, 0)

    evol = []

    # Main body
    population = brkga.initializePopulation(numIndividuals, chrLength)

    i = 0
    while (i<maxNumGen):
        population = decoder.decode(population,data)
        evol.append(brkga.getBestFitness(population)['fitness'])
        print(evol[-1])
        if numElite>0:
            elite, nonelite = brkga.classifyIndividuals(population,numElite)
        else: 
            elite = []
            nonelite = population
        if numMutants>0: mutants = brkga.generateMutantIndividuals(numMutants,chrLength)
        else: mutants = []
        if numCrossover>0: crossover = brkga.doCrossover(elite,nonelite,ro,numCrossover)
        else: crossover=[]
        population=elite + crossover + mutants
        i+=1
        
    population = decoder.decode(population, data)
    bestIndividual = brkga.getBestFitness(population)


    #pp.pprint(data)
    #print(bestIndividual["solution"])
    print('Fitness: ', bestIndividual['fitness'])
    # pp.pprint(bestIndividual.keys())
    # pp.pprint(bestIndividual['solution'].keys())
    return bestIndividual["solution"]

if __name__ == '__main__':

    # initializations
    numIndividuals = int(config['numIndividuals'])
    numElite = int(math.ceil(numIndividuals * config['eliteProp']))
    numMutants = int(math.ceil(numIndividuals * config['mutantProp']))
    numCrossover = max(numIndividuals - numElite - numMutants, 0)
    maxNumGen = int(config['maxNumGen'])
    ro = float(config['inheritanceProb'])
    evol = []

    # must be derived from instance
    chrLength = int(config['chromosomeLength'])

    # Main body

    population = brkga.initializePopulation(numIndividuals, chrLength)

    i=0
    while (i<maxNumGen):
        population = decoder.decode(population,data)
        evol.append(brkga.getBestFitness(population)['fitness'])
        if numElite>0:
            elite, nonelite = brkga.classifyIndividuals(population,numElite)
        else: 
            elite = []
            nonelite = population
        if numMutants>0: mutants = brkga.generateMutantIndividuals(numMutants,chrLength)
        else: mutants = []
        if numCrossover>0: crossover = brkga.doCrossover(elite,nonelite,ro,numCrossover)
        else: crossover=[]
        population=elite + crossover + mutants
        i+=1
        
    population = decoder.decode(population, data)
    bestIndividual = brkga.getBestFitness(population)
    plt.plot(evol)
    plt.xlabel('number of generations')
    plt.ylabel('Fitness of best individual')
    plt.axis([0, len(evol), 0, (chrLength+1)*chrLength/2])
    plt.show()


