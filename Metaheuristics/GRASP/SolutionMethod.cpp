#include <iostream>
#include "Problem.cpp"
#include "Solution.cpp"
using namespace std;
#pragma once

class SolutionMethod {
    protected:
        int iteration = 0;
        long elapsedTime;
    protected:
        inline int getIteration() const { return iteration; }
        inline long getElapsedTime() const { return elapsedTime; }
        inline void setIteration(int iteration) { this->iteration = iteration; }
        inline void setElapsedTime(long elapsedTime) { this->elapsedTime = elapsedTime; }
        inline void resetIteration() { this->iteration = 0; }
    public:
        virtual void performSearch() = 0;
};