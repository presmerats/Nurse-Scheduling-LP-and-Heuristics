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
    double evaluate(const Solution* s);
    bool isFeasible(Solution* s);
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

double NurseSchedulingProblem::evaluate(const Solution* s) {
    auto nurseSchedulingSolution = dynamic_cast<const NurseSchedulingSolution*>(s);
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

bool NurseSchedulingProblem::isFeasible(Solution* s) {
    auto nurseSchedulingSolution = dynamic_cast<NurseSchedulingSolution*>(s);

    std::vector< std::vector<bool> > assignments = nurseSchedulingSolution->getAssignments();

    for(int i = 0; i < getNumNurses(); i++) {
        int hoursWorked = 0;
        bool nurseAlreadyStarted = false;
        int nurseTotalPresence = 0;
        for(int j = 0; j < 24; j++) {
            if(assignments[i][j] == true) {
                nurseAlreadyStarted = true;
                hoursWorked++;
                nurseTotalPresence++;
                if(hoursWorked > getMaxHours()) return false;
            }

            if(nurseAlreadyStarted == true) {
                nurseTotalPresence++;
                if(nurseTotalPresence > getMaxPresence()) return false;
            }

            if(j > 0) {
                // Get the working runs
                int workingRun = 0;
                int restRun = 0;
                for(int k = 0; k == j; k++) {
                    if(assignments[i][k] == true) {
                        restRun = 0;
                        workingRun++;
                        if(workingRun > getMaxConsec()) return false;
                    } else {
                        workingRun = 0;
                        restRun++;
                        if(restRun > 1) return false;
                    }
                }
            }
        }
    }

    // Demand is accomplished
    for(int j = 0; j < 24; j++) {
        int totalNurses = 0;
        for(int i = 0; i < getNumNurses(); i++) {
            if(nurseSchedulingSolution->containsElement(i,j)) totalNurses++;
        }
        if(totalNurses < getDemand().at(j)) return false;
    }

    return true;
}