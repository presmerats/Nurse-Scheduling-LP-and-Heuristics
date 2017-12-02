#include <iostream>
using namespace std;

class SolutionMethod {
    private:
        int iteration = 0;
        long elapsedTime;
        Problem problem;
        Solution bestSolution;
    protected:
        inline int getIteration() const { return iteration; }
        inline long getElapsedTime() const { return elapsedTime; }
        inline void setIteration(int iteration) { this->iteration = iteration; }
        inline void setElapsedTime(long elapsedTime) { this->elapsedTime = elapsedTime; }
        inline void resetIteration() { this->iteration = 0; }
        inline Problem getProblem() const { return problem; }
        inline Solution getSolution() const { return solution; }
        inline void setProblem(const Problem problem) { this->problem = problem; }
        inline void setSolution(const Solution solution) { this->solution = solution; }
};