#include <iostream>
using namespace std;

class Problem {
  public:
    virtual ~Problem() {}
    virtual void read() = 0;
    virtual double evaluate(const Solution& s) = 0;
};