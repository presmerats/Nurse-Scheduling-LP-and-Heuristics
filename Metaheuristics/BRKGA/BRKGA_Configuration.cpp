#include <iostream>
using namespace std;
#pragma once

class BRKGA_Configuration {
    private:
        int chromosomeLength;
        int numberIndividuals;
        int maxNumGenerations;
        float eliteProp;
        float mutantProp;
        float inheritanceProb;
    public:
        BRKGA_Configuration(int,int,int,float,float,float);
        ~BRKGA_Configuration();
        inline int getChromosomeLength() { return chromosomeLength; }
        inline int getNumberIndividuals() { return numberIndividuals; }
        inline int getMaxNumGenerations() { return maxNumGenerations; }
        inline float getEliteProp() { return eliteProp; }
        inline float getMutantProp() { return mutantProp; }
        inline float getInheritanceProb() { return inheritanceProb; }
        inline void setChromosomeLength(int chromosomeLength) { this->chromosomeLength = chromosomeLength; }
        inline void setNumberIndividuals(int numberIndividuals) { this->numberIndividuals = numberIndividuals; }
        inline void setMaxNumGenerations(int maxNumGenerations) { this->maxNumGenerations = maxNumGenerations; }
        inline void setEliteProp(float eliteProp) { this->eliteProp = eliteProp; }
        inline void setMutantProp(float mutantProp) { this->mutantProp = mutantProp; }
        inline void setInheritanceProb(float inheritanceProb) { this->inheritanceProb = inheritanceProb; }
};

BRKGA_Configuration::BRKGA_Configuration(int chromosomeLength, int numberIndividuals, int maxNumGenerations, float eliteProp, float mutantProp, float inheritanceProb) {
    this->chromosomeLength = chromosomeLength;
    this->numberIndividuals = numberIndividuals;
    this->maxNumGenerations = maxNumGenerations;
    this->eliteProp = eliteProp;
    this->mutantProp = mutantProp;
    this->inheritanceProb = inheritanceProb;
}

BRKGA_Configuration::~BRKGA_Configuration() {
    this->chromosomeLength = 0;
    this->numberIndividuals = 0;
    this->maxNumGenerations = 0;
    this->eliteProp = 0;
    this->mutantProp = 0;
    this->inheritanceProb = 0;
}