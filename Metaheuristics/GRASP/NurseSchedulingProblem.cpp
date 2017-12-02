#include <iostream>
#include <vector>
#include "Problem.cpp"
using namespace std;

class NurseSchedulingProblem: public Problem {
  private:
    string filePath;
    int numNurses;
    int minHours;
    int maxHours;
    int maxConsec;
    int maxPresence;
    std::vector<int> demand;

  public:
    NurseSchedulingProblem();
    NurseSchedulingProblem(string);
    inline void setFilePath(string filePath) { this->filePath = filePath; };
    inline string getFilePath() const { return filePath; }
    void read();
};

NurseSchedulingProblem::NurseSchedulingProblem() {
    this->filePath = "";
    this->numNurses = 0;
    this->minHours = 0;
    this->maxHours = 0;
    this->maxConsec = 0;
    this->maxPresence = 0;
    demand.reserve(24);
    for(int i = 0; i < demand.size(); i++) {
        demand[i] = 0;
    }
}

NurseSchedulingProblem::NurseSchedulingProblem(string filePath) {
    this->filePath = filePath;
}
void NurseSchedulingProblem::read() {
    // Read from file
}