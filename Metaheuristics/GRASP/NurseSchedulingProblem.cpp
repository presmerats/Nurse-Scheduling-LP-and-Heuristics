#include <iostream>
#include <vector>
#include <algorithm>
#include "Problem.cpp"
using namespace std;
#pragma once

class NurseSchedulingProblem: public Problem {
  private:
    string filePath;
    int numNurses;
    int minHours;
    int maxHours;
    int maxConsec;
    int maxPresence;
    std::vector<int> demand;

  public:
    NurseSchedulingProblem();
    NurseSchedulingProblem(string);
    inline void setFilePath(string filePath) { this->filePath = filePath; };
    inline string getFilePath() const { return filePath; }
    void read();
    double evaluate(const Solution& s);
    inline int getNumNurses() { return numNurses; }
    inline int getMinHours() { return minHours; }
    inline int getMaxHours() { return maxHours; }
    inline int getMaxConsec() { return maxConsec; }
    inline int getMaxPresence() { return maxPresence; }
    inline std::vector<int> getDemand() { return demand; }
};

NurseSchedulingProblem::NurseSchedulingProblem() {
    this->filePath = "";
    this->numNurses = 0;
    this->minHours = 0;
    this->maxHours = 0;
    this->maxConsec = 0;
    this->maxPresence = 0;
    demand.reserve(24);
    for(int i = 0; i < demand.size(); i++) {
        demand[i] = 0;
    }
}

NurseSchedulingProblem::NurseSchedulingProblem(string filePath) {
    this->filePath = filePath;
}
void NurseSchedulingProblem::read() {
    // Read from file
}

double NurseSchedulingProblem::evaluate(const Solution& s) {
    auto nurseSchedulingSolution = dynamic_cast<const NurseSchedulingSolution*>(&s);
    // The objective is to minimize the number of working nurses
    std::vector< std::vector<bool> > solutionAssignments = nurseSchedulingSolution->getAssignments();
    int workingNurses = 0;
    for(int i = 0; i < numNurses; i++) {
        std::vector<bool>::iterator it = find (solutionAssignments.at(i).begin(), solutionAssignments.at(i).end(), true);
        if(it != solutionAssignments.at(i).end()) {
            workingNurses++;
        }
    }
    return workingNurses;
}