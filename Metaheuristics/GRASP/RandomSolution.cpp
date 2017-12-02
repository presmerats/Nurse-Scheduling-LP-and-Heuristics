#include <iostream>
#include "SolutionGenerator.cpp"
using namespace std;

class RandomSolution: public SolutionGenerator {
    private:
        int numNurses;
    public:
        RandomSolution(int);
        NurseSchedulingSolution generate();
        inline int getNumNurses() { return numNurses; }
        inline void setNumNurses(int numNurses) { this->numNurses = numNurses; }
};

RandomSolution::RandomSolution(int numNurses) {
    this->numNurses = numNurses;
}

RandomSolution::generate() {
    NurseSchedulingSolution randomSolution(getNumNurses(),0);
    srand(time(0));
    for(int i = 0; i < getNumNurses(); ++i )
    {
        for(int j = 0; j < 24; j++) {
            bool state = rand() % 2;
            randomSolution.setElement(i,j,state);
        }
    }

    return randomSolution;
}