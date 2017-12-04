#include <iostream>
#include <ctime>
#include <algorithm>
#include <cmath>
#include "Individual.cpp"
#include "BRKGA_Configuration.cpp"
using namespace std;
#pragma once

class BRKGA {
    private:
        BRKGA_Configuration config;
    public:
        BRKGA(BRKGA_Configuration);
        ~BRKGA();
        std::vector<Individual> initializePopulation();
        pair<std::vector<Individual>, std::vector<Individual> > classifyIndividuals(std::vector<Individual>,int);
        std::vector<Individual> generateMutantIndividuals(int);
        std::vector<Individual> doCrossover(std::vector<Individual>,std::vector<Individual>,float,int);
        double getBestFitness(std::vector<Individual>);
        inline BRKGA_Configuration getConfig() { return this->config; }
};

BRKGA::BRKGA(BRKGA_Configuration config)
{
    srand (static_cast <unsigned> (time(0)));
    this->config = config;
}

BRKGA::~BRKGA()
{
}

std::vector<Individual> BRKGA::doCrossover(std::vector<Individual> elite,std::vector<Individual> nonElite,float ro,int numCrossover)
{
    std::vector<Individual> crossover;

    for(int i = 0; i < numCrossover; i++) {
        float r = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
        int indexElite = (int)floor(r * elite.size());

        r = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
        int indexNonElite = (int)floor(r * nonElite.size());

        std::vector<float> eliteChromosome = elite.at(indexElite).getChromosome();
        std::vector<float> nonEliteChromosome = nonElite.at(indexNonElite).getChromosome();

        std::vector<float> randomChromosome;
        randomChromosome.reserve(eliteChromosome.size());
        for(int j = 0; j < eliteChromosome.size(); j++) {
            float randomGene = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            randomChromosome[j] = randomGene;
        }

        std::vector<float> crossedChromosome;
        crossedChromosome.reserve(eliteChromosome.size());

        for(int j = 0; j < eliteChromosome.size(); j++) {
            if(randomChromosome.at(j) <= ro) {
                crossedChromosome[j] = eliteChromosome[j];
            } else {
                crossedChromosome[j] = nonEliteChromosome[j];
            }
        }

        Individual crossedIndividual(crossedChromosome);
        crossover.push_back(crossedIndividual);
    }

    return crossover;
}

pair<std::vector<Individual>, std::vector<Individual> > BRKGA::classifyIndividuals(std::vector<Individual> population,int numElites)
{
    std::vector<double> fitnessOfPopulationIndividuals;
    for(int i = 0; i < population.size(); i++) {
        fitnessOfPopulationIndividuals.push_back(population.at(i).getFitness());
        std::sort(fitnessOfPopulationIndividuals.begin(), fitnessOfPopulationIndividuals.end(), std::greater<float>());
    }

    std::vector<double> whichElite(fitnessOfPopulationIndividuals.begin(), fitnessOfPopulationIndividuals.begin() + numElites);
    std::vector<double> whichNonElite(fitnessOfPopulationIndividuals.begin() + numElites, fitnessOfPopulationIndividuals.begin() + numElites + fitnessOfPopulationIndividuals.size());

    std::vector<Individual> elite;
    std::vector<Individual> nonElite;

    for(int i = 0; i < whichElite.size(); i++) {
        for(int j = 0; j < population.size(); j++) {
            if(population.at(j).getFitness() == whichElite.at(i)) {
                elite.push_back(population.at(j));
                population.erase(population.begin() + j);
                break;
            }
        }
    }

    for(int i = 0; i < whichNonElite.size(); i++) {
            for(int j = 0; j < population.size(); j++) {
                if(population.at(j).getFitness() == whichNonElite.at(i)) {
                    nonElite.push_back(population.at(j));
                    population.erase(population.begin() + j);
                    break;
                }
            }
        }

    pair<std::vector<Individual>, std::vector<Individual> > classification(elite, nonElite);
    return classification;
}

double BRKGA::getBestFitness(std::vector<Individual> population)
{
    std::vector<double> fitnessOfPopulationIndividuals;
    //population.reserve(this->getConfig().getNumberIndividuals());

    for(int i = 0; i < population.size(); i++) {
        fitnessOfPopulationIndividuals.push_back(population.at(i).getFitness());
        std::sort(fitnessOfPopulationIndividuals.begin(), fitnessOfPopulationIndividuals.end(), std::greater<float>());
    }

    return fitnessOfPopulationIndividuals.at(0);
}

std::vector<Individual> BRKGA::generateMutantIndividuals(int numMutants)
{
    std::vector<Individual> mutants;
    //population.reserve(this->getConfig().getNumberIndividuals());

    for(int i = 0; i < numMutants; i++) {
        std::vector<float> chromosome;
        chromosome.reserve(this->getConfig().getChromosomeLength());
        for(int j = 0; j < this->getConfig().getChromosomeLength(); j++) {
            float r = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            chromosome[j] = r;
        }
        Individual mutant(chromosome);
        mutants.push_back(mutant);
    }

    return mutants;
}

std::vector<Individual> BRKGA::initializePopulation()
{
    std::vector<Individual> population;
    //population.reserve(this->getConfig().getNumberIndividuals());

    for(int i = 0; i < this->getConfig().getNumberIndividuals(); i++) {
        std::vector<float> chromosome;
        chromosome.reserve(this->getConfig().getChromosomeLength());
        for(int j = 0; j < this->getConfig().getChromosomeLength(); j++) {
            float r = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            chromosome[j] = r;
        }
        Individual ind(chromosome);
        population.push_back(ind);
    }

    return population;
}