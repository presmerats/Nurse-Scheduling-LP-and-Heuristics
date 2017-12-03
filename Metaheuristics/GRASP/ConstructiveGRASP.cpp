#include <iostream>
#include <tuple>        // std::tuple, std::get, std::tie, std::ignore
#include <algorithm>
#include <vector>
#include "SolutionMethod.cpp"
using namespace std;

struct CandidateAssignment {
    int nurse;
    int hour;
    bool state;
    double cost;
};

class ConstructiveGRASP: public SolutionMethod {
    private:
        int RCLsize;
        NurseSchedulingSolution* currentSolution;
        NurseSchedulingProblem* problem;
        NurseSchedulingSolution* bestSolution;
    public:
        ConstructiveGRASP(NurseSchedulingProblem*,int,int);
        void performSearch();
        NurseSchedulingSolution* constructSolution(float alpha);
        NurseSchedulingSolution* localSearch();
        std::vector<CandidateAssignment> createAssignmentsNotInSolution(NurseSchedulingSolution*);
        std::vector<CandidateAssignment> updateCandidatesSet(NurseSchedulingSolution*,std::vector<CandidateAssignment>);
        std::vector<CandidateAssignment> initializeCandidatesSet();
        double computeGreedyCost(int,int,bool);
        inline void setRCLsize(int RCLsize) { this->RCLsize = RCLsize; }
        inline void setCurrentSolution(NurseSchedulingSolution* currentSolution) { this->currentSolution = currentSolution; }
        inline NurseSchedulingProblem* getProblem() const { return problem; }
        inline NurseSchedulingSolution* getSolution() const { return bestSolution; }
        inline void setProblem(NurseSchedulingProblem* problem) { this->problem = problem; }
        inline void setSolution(NurseSchedulingSolution* solution) { this->currentSolution = solution; }
};

ConstructiveGRASP::ConstructiveGRASP(NurseSchedulingProblem* problem, int RCLsize, int maxIterations) {
    this->problem = problem;
    this->RCLsize = RCLsize;
    this->currentSolution = new NurseSchedulingSolution(getProblem()->getNumNurses(), 0);
    this->problem->setMaxIterations(maxIterations);
}

void ConstructiveGRASP::performSearch() {
    int iteration = 0;

    for(int i = 0; i < getProblem()->getMaxIterations(); i++) {
        //ConstructSolution
        //LocalSearch
    }
}

NurseSchedulingSolution* ConstructiveGRASP::constructSolution(float alpha) {
    NurseSchedulingSolution* solution = new NurseSchedulingSolution(getProblem()->getNumNurses(), 0);

    //Initialize candidate set C
    std::vector<CandidateAssignment> candidates = initializeCandidatesSet();
    while(!candidates.empty()) {
        // s
        auto minGreedyAssignment = std::min_element( candidates.begin(), candidates.end(),
                                     []( const CandidateAssignment &a, const CandidateAssignment &b )
                                     {
                                         return a.cost > b.cost;
                                     } );

        // s'
        auto maxGreedyAssignment = std::max_element( candidates.begin(), candidates.end(),
                                             []( const CandidateAssignment &a, const CandidateAssignment &b )
                                             {
                                                 return a.cost < b.cost;
                                             } );

        double minGreedyAssignmentCost = (*minGreedyAssignment).cost;
        double maxGreedyAssignmentCost = (*maxGreedyAssignment).cost;

        std::vector<CandidateAssignment> restrictedCandidatesList;

        for(int i = 0; i < candidates.size(); i++) {
            auto candidate = candidates.at(i);
            double candidateGreedyCost = candidate.cost;
            if(candidateGreedyCost <= minGreedyAssignmentCost + alpha * (maxGreedyAssignmentCost - minGreedyAssignmentCost)) {
                restrictedCandidatesList.push_back(candidate);
            }
        }

        // Select new assignment candidate to add, at random, from he RCL
        std::random_shuffle(&restrictedCandidatesList[0], &restrictedCandidatesList[restrictedCandidatesList.size()-1]);
        auto candidateToAdd = restrictedCandidatesList.at(0);

        // Assign it
        solution->setElement(candidateToAdd.nurse,candidateToAdd.hour,candidateToAdd.state);
        candidates = updateCandidatesSet(solution, candidates);

    }

    return solution;
}

NurseSchedulingSolution* ConstructiveGRASP::localSearch() {
    bool update = true;
    while(update) {

    }
}

std::vector<CandidateAssignment> ConstructiveGRASP::updateCandidatesSet(NurseSchedulingSolution* solution, std::vector<CandidateAssignment> candidates) {
    std::vector<int> unfeasibleNurses;
    std::vector< std::vector<bool> > assignments = solution->getAssignments();

    for(int i = 0; i < getProblem()->getNumNurses(); i++) {
        int hoursWorked = 0;
        bool nurseAlreadyStarted = false;
        int nurseTotalPresence = 0;
        std::vector<int> workingRunsLength;
        for(int j = 0; j < 24; j++) {
            if(assignments[i][j] == true) {
                nurseAlreadyStarted = true;
                hoursWorked++;
                nurseTotalPresence++;
            }

            if(nurseAlreadyStarted == true) { nurseTotalPresence++; }

            if(j > 0) {
                // Get the working runs
                int workingRun = 0;
                for(int k = 0; k == j; k++) {
                    if(assignments[i][k] == true) {
                        workingRun++;
                    } else {
                        workingRunsLength.push_back(workingRun);
                        workingRun = 0;
                    }
                }
            }
        }

        // Check feasibility
        // 1. Nurses must work at most maxHours
        if(hoursWorked >= getProblem()->getMaxHours()) {
            unfeasibleNurses.push_back(i);
            continue;
        }

        // 2. Nurses must work at most maxConsec hours
        auto maxWorkingRun = max_element(std::begin(workingRunsLength), std::end(workingRunsLength));
        if(*maxWorkingRun >= getProblem()->getMaxConsec()) {
            unfeasibleNurses.push_back(i);
            continue;
        }

        // 3. Nurses must be at most maxPresence hours at the hospital
        if(nurseTotalPresence >= getProblem()->getMaxPresence()) {
            unfeasibleNurses.push_back(i);
            continue;
        }
    }

    // Remove unfeasible nurses from candidates
    candidates.erase( std::remove_if( candidates.begin(), candidates.end(), [&](CandidateAssignment const& ca) { return std::find(unfeasibleNurses.begin(), unfeasibleNurses.end(), ca.nurse) != unfeasibleNurses.end(); }), candidates.end());

    return candidates;
}

std::vector<CandidateAssignment> ConstructiveGRASP::initializeCandidatesSet() {
    std::vector<CandidateAssignment> candidates;

    for(int i = 0; i < getProblem()->getNumNurses(); i++) {
        for(int j = 0; j < 24; j++) {
            double greedyCostOfTrueAssignment = computeGreedyCost(i,j,true);
            double greedyCostOfFalseAssignment = computeGreedyCost(i,j,false);

            CandidateAssignment candidateTrue = {i,j,true,greedyCostOfTrueAssignment};
            CandidateAssignment candidateFalse = {i,j,false,greedyCostOfFalseAssignment};

            candidates.push_back(candidateTrue);
            candidates.push_back(candidateFalse);
        }
    }

    return candidates;
}

std::vector<CandidateAssignment> ConstructiveGRASP::createAssignmentsNotInSolution(NurseSchedulingSolution* solution) {
    std::vector<CandidateAssignment> assignmentsNotInSolution;

    for(int i = 0; i < getProblem()->getNumNurses(); i++) {
        for(int j = 0; j < 24; j++) {
            if(solution->getAssignments()[i][j] == true) continue;

                double greedyCostOfAssignment = computeGreedyCost(i,j,true);
                CandidateAssignment candidateAssignment = {i,j,true,greedyCostOfAssignment};
                assignmentsNotInSolution.push_back(candidateAssignment);
        }
    }

    return assignmentsNotInSolution;
}

double ConstructiveGRASP::computeGreedyCost(int nurse, int hour, bool state) {
    // Just a dummy test of greedy cost calculation
    return (nurse / hour) - (int)state;
}