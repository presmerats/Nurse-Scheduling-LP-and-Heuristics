

"""
    this script 
        1- takes instances from ../../Instances/Pending
    and then for each instance:
        2- prepares a .mod file that executes the instance and writes to a log file in ../../Results/Pending/log-<instance>.json
        3- that .mod file must save a key value "solver" : "ILP" inside the written json file
    executes
        4- executes in shell the command "oplrun -v <name>.mod" with the env var LD_LIBRARY_PATH=/opt/ibm/ILOG/CPLEX_Studio126/opl/bin/x86-64_linux

"""