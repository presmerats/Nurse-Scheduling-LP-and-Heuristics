#include <iostream>
using namespace std;
#pragma once

class Problem {
  protected:
    int maxIterations;
  public:
    inline int getMaxIterations() { return maxIterations; }
    inline void setMaxIterations(int maxIterations) { this->maxIterations = maxIterations; }
    virtual ~Problem() {}
    virtual void read() = 0;
    virtual double evaluate(const Solution& s) = 0;
};