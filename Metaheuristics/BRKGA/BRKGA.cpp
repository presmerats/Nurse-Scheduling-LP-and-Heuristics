#include <iostream>
#include <ctime>
#include <algorithm>
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
        pair<std::vector<Individual>, std::vector<Individual> > classifyIndividuals(std::vector<Individual>);
        std::vector<Individual> generateMutantIndividuals(int);
        std::vector<Individual> doCrossover(std::vector<Individual> elite,std::vector<Individual> nonElite,float,int);
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