#include <iostream>
using namespace std;

class NurseSchedulingSolution {
    double value = 0;
  public:
    void setValue (double);
    inline double getValue() { return value; }
};

void Solution::setValue (double value) {
  this->value = value;
}