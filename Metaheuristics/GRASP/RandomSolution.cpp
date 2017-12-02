#include <iostream>
#include "SolutionGenerator.cpp"
using namespace std;

class RandomSolution: public SolutionGenerator {
    public:
        NurseSchedulingSolution generate(int);
};

RandomSolution::generate(int numNurses) {
    NurseSchedulingSolution randomSolution(numNurses,0);
    srand(time(0));
    for(int i = 0; i < numNurses; ++i )
    {
        for(int j = 0; j < 24; j++) {
            bool state = rand() % 2;
            randomSolution.setElement(i,j,state);
        }
    }

    return randomSolution;
}