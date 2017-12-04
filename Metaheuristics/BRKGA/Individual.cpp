#include <iostream>
#include <vector>
#include "NurseAssignment.cpp"
using namespace std;
#pragma once

class Individual {
    private:
        std::vector<float> chromosome;
        std::vector<NurseAssignment> solution;
        double fitness;
    public:
        Individual();
        Individual(std::vector<float>, std::vector<NurseAssignment>, double);
        ~Individual();
        inline std::vector<float> getChromosome() { return this->chromosome; }
        inline std::vector<NurseAssignment> getSolution() { return this->solution; }
        inline double getFitness() { return this->fitness; }
        inline void setChromosome(std::vector<float> chromosome) { this->chromosome = chromosome; }
        inline void setSolution(std::vector<NurseAssignment> solution) { this->solution = solution; }
        inline void setFitness(double fitness) { this->fitness = fitness; }
};

Individual::Individual() {
    this->fitness = 0.0;
}

Individual::Individual(std::vector<float> chromosome, std::vector<NurseAssignment> solution, double fitness) {
    this->chromosome = chromosome;
    this->solution = solution;
    this->fitness = fitness;
}

Individual::~Individual() {
    this->chromosome.clear();
    this->solution.clear();
    this->fitness = 0.0;
}