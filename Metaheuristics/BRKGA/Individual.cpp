#include <iostream>
using namespace std;
#pragma once

class Individual {
    private:
        int value;
    public:
        inline int getValue() { return value; }
        inline void setValue(int value) { this->value = value; }
};