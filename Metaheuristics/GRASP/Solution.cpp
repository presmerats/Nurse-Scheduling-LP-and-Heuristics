#include <iostream>
using namespace std;

class Solution {
  protected:
    double value = 0;
  public:
    virtual ~Solution() {}
    void setValue (double);
    inline double getValue() const { return value; }
    virtual bool operator==(const Solution& s) { return false; }
};

void Solution::setValue (double value) {
  this->value = value;
}