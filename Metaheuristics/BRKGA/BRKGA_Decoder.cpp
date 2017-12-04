#include <iostream>
#include <vector>
#include "Individual.cpp"
using namespace std;
#pragma once

class BRKGA_Decoder {
    static std::vector<Individual> decode(std::vector<Individual> population);
};

std::vector<Individual> BRKGA_Decoder::decode(std::vector<Individual> population)
{
   for(auto i : population) {
       population[0].setFitness(0);
       population[1].setFitness(1);
   }

   return population;
}