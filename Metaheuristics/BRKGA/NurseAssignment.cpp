#include <iostream>
using namespace std;
#pragma once

class NurseAssignment {
    private:
        int nurseId;
        int hour;
        bool state;
    public:
        NurseAssignment(int,int,bool);
        ~NurseAssignment();
        inline int getNurseId() { return nurseId; }
        inline int getHour() { return hour; }
        inline bool getState() { return state; }
        inline void setNurseId(int nurseId) { this->nurseId = nurseId; }
        inline void setHour(int hour) { this->hour = hour; }
        inline void setState(bool state) { this->state = state; }
};

NurseAssignment::NurseAssignment(int nurseId, int hour, bool state) {
    this->nurseId = nurseId;
    this->hour = hour;
    this->state = state;
}

NurseAssignment::~NurseAssignment() {
    this->nurseId = 0;
    this->hour = 0;
    this->state = false;
}