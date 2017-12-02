#include <iostream>
using namespace std;

class AddMovement {
    NurseSchedulingSolution perform(NurseSchedulingSolution&, int, int);
};

AddMovement::perform(NurseSchedulingSolution& solution, int nurse, int hour) {
    solution.addElement(nurse,hour);
    return solution;
}