#include <iostream>
#include <vector>
#include "Solution.cpp"
using namespace std;

class NurseSchedulingSolution: public Solution {
  private:
    std::vector< std::vector<bool> > assignments;
  public:
    NurseSchedulingSolution();
    NurseSchedulingSolution(double);
    NurseSchedulingSolution(int, double);
    NurseSchedulingSolution(std::vector< std::vector<bool> >, double);
    inline void setAssignments(std::vector< std::vector<bool> > assignments) { this->assignments = assignments; };
    inline std::vector< std::vector<bool> > getAssignments() const { return assignments; }
    void addElement(int,int);
    void removeElement(int,int);
    void flipElement(int,int);
    bool containsElement(int,int);
    bool operator ==(const Solution& s) override {
        auto other = dynamic_cast<const NurseSchedulingSolution*>(&s);
        return other != 0 && getAssignments() == other->getAssignments() && getValue() == other->getValue();
    }
};

NurseSchedulingSolution::NurseSchedulingSolution() {
    this->value = 0;
}

NurseSchedulingSolution::NurseSchedulingSolution(double value) {
    this->value = value;
}

NurseSchedulingSolution::NurseSchedulingSolution(int numNurses, double value) {
    this->value = value;
    assignments.resize(numNurses);
    for(int i = 0 ; i < numNurses ; i++)
    {
        assignments[i].resize(24);
    }
}

NurseSchedulingSolution::NurseSchedulingSolution(std::vector< std::vector<bool> > assignments, double value) {
    this->value = value;
    this->assignments = assignments;
}

void NurseSchedulingSolution::addElement(int nurse, int hour) {
    this->assignments[nurse][hour] = true;
}

void NurseSchedulingSolution::removeElement(int nurse, int hour) {
    this->assignments[nurse][hour] = false;
}

void NurseSchedulingSolution::flipElement(int nurse, int hour) {
    this->assignments[nurse][hour] = !this->assignments[nurse][hour];
}

bool NurseSchedulingSolution::containsElement(int nurse, int hour) {
    return this->assignments[nurse][hour];
}