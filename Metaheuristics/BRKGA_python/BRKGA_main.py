# imports
import math
import matplotlib.pyplot as plt

import BRKGA as brkga
import DECODER as decoder
from DATA_DUMMY import data
from CONFIGURATION import config


def brkga_run(data):

    # initializations

    # must be derived from instance
    chrLength = int(data["nNurses"])
    numIndividuals = int(config['a']) * int(data["nNurses"])

    numElite = int(math.ceil(numIndividuals * config['eliteProp']))
    numMutants = int(math.ceil(numIndividuals * config['mutantProp']))
    numCrossover = max(numIndividuals - numElite - numMutants, 0)
    maxNumGen = int(config['maxNumGen'])
    ro = float(config['inheritanceProb'])
    evol = []

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

    return bestIndividual

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


