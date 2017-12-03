#include <iostream>
using namespace std;
#pragma once

class AddMovement: public Movement {
    NurseSchedulingSolution perform(NurseSchedulingSolution&, int, int);
};

NurseSchedulingSolution AddMovement::perform(NurseSchedulingSolution& solution, int nurse, int hour) {
    solution.addElement(nurse,hour);
    return solution;
}