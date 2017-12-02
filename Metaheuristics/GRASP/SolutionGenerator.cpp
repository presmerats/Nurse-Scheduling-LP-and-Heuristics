#include <iostream>
#include "NurseSchedulingSolution.cpp"
using namespace std;

class SolutionGenerator {
    virtual NurseSchedulingSolution generate() = 0;
};