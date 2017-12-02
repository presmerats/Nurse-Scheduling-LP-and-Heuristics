#include <iostream>
#include "NurseSchedulingSolution.cpp"
using namespace std;

class Movement {
    virtual NurseSchedulingSolution perform(const NurseSchedulingSolution&, int, int) = 0;
};