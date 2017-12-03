#include <iostream>
#include <tuple>        // std::tuple, std::get, std::tie, std::ignore
#include <algorithm>
#include <vector>
#include "SolutionMethod.cpp"
#include "Movement.cpp"
#include "AddMovement.cpp"
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
        Movement* move = new AddMovement();
        NurseSchedulingProblem* problem;
        NurseSchedulingSolution* bestSolution;
    public:
        ConstructiveGRASP(NurseSchedulingProblem*,int,int);
        void performSearch();
        NurseSchedulingSolution* constructSolution(float alpha);
        NurseSchedulingSolution* localSearch();
        std::vector<CandidateAssignment> updateCandidatesSet(NurseSchedulingSolution*,std::vector<CandidateAssignment>);
        std::vector<CandidateAssignment> initializeCandidatesSet();
        double computeGreedyCost(int,int,bool);
        inline void setRCLsize(int RCLsize) { this->RCLsize = RCLsize; }
        inline void setCurrentSolution(NurseSchedulingSolution* currentSolution) { this->currentSolution = currentSolution; }
        inline void setMove(Movement* move) { this->move = move; }
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
    this->move = new AddMovement();
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

std::vector<CandidateAssignment> ConstructiveGRASP::updateCandidatesSet(NurseSchedulingSolution* solution, std::vector<CandidateAssignment> candidates) {
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

double ConstructiveGRASP::computeGreedyCost(int nurse, int hour, bool state) {
    // Just a dummy test of greedy cost calculation
    return (nurse / hour) - (int)state;
}