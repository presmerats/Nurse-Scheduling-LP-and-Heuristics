#include <iostream>
#include <ctime>
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
        std::vector<Individual> generateMutantIndividuals();
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
        population.push_back(chromosome);
    }

    return population;
}