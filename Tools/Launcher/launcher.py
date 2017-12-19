import json
import sys
import os
import traceback
import shutil
import re
from subprocess import call,check_call,Popen, PIPE
from pathlib import Path, PurePath

parentPath = os.path.abspath("../../Metaheuristics/GRASP_python")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

import main as grasp


"""
    this script 
        1- takes instances from ../../Instances/Pending
    and then for each instance:
        2- prepares a .mod file that executes the instance and writes to a log file in ../../Results/Pending/log-<instance>.json
        3- that .mod file must save a key value "solver" : "ILP" inside the written json file
    executes
        4- executes in shell the command "oplrun -v <name>.mod" with the env var LD_LIBRARY_PATH=/opt/ibm/ILOG/CPLEX_Studio126/opl/bin/x86-64_linux

"""
mod_header_template = os.path.abspath('../Instance_Generator/Complex Generator/Test-header2.template')
mod_footer_template = os.path.abspath('../Instance_Generator/Complex Generator/Test-footer.template')


def shellexec(command, cwd="."):

    my_env = os.environ.copy()
    if my_env["PATH"].find("/usr/sbin:/sbin:") < 0:
        my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]

    my_env["LD_LIBRARY_PATH"] = "/opt/ibm/ILOG/CPLEX_Studio126/opl/bin/x86-64_linux"

    p = Popen(
        [command],
        cwd=cwd,
        shell=True,
        env=my_env,
        stdout=PIPE,
        stderr=PIPE)

    (out, err) = p.communicate()

    return (out, err)


def prepareModFile(instancepath, tilim=1800.0,  path=Path()):
    print("preparing mod file for :" + instancepath)

    filename = '../../Tools/Launcher/temp.mod'
    filename = PurePath(path, filename)

    modelfile = '../../ILP/model01.mod'
    modelfile = os.path.abspath(modelfile)

    logfile = os.path.splitext(os.path.basename(instancepath))[0] + '.json'
    logname = '../../Results/Pending/' + logfile

    with open(filename, 'w') as f:

        with open(mod_header_template, 'r') as h:
            for line in h:
                if "model01-hfree.mod" in line:
                    line = line.replace("model01-hfree.mod", str(modelfile))

                if line.startswith("var logname = \""):

                    line = "var logname = \"" + logname + "\";\n"

                f.write(line)

        f.write(
            'myTest(def, cplex,"' +
            instancepath +
            '", logname, ' +
            str(tilim) +
            ',  "SUCCESS", 1 );\n')

        with open(mod_footer_template,'r') as h:
            for line in h:
                f.write(line)

    return str(filename)


def solveInstanceWithILP(instancepath):

    modfile = prepareModFile(instancepath)

    print("solving instance " + modfile)
    output, error = shellexec("oplrun -v " + modfile)
    print("output = ")
    print(output)


def acceptInstance(instance):

    i1 = instance.find('-')
    time_it_takes_to_solve = -1
    try:
        time_it_takes_to_solve = int(instance[:i1])
    except:
        time_it_takes_to_solve = sys.maxsize

    return time_it_takes_to_solve < 3



if __name__ == '__main__':

    instances_folder = "../../Instances/Pending/"

    if len(sys.argv) > 1:

        solverType = sys.argv[1]

        if solverType not in ["ILP", "greedy", "grasp", "brkga"]:
            print("Usage: python main.py <metaheuristic_algorithm>")
            exit()
    else:
        solverType = "ILP"

    instanceType = 'all'
    if len(sys.argv) > 2:
        instanceType = sys.argv[2]

    if len(sys.argv) > 3:
        instances_folder = sys.argv[3]

    if not os.path.exists(instances_folder):
        print("check folder paths!")
        exit()

    os.chdir(instances_folder)
    for root, dirs, files in os.walk("."):
        all_ok = True
        for instance in files:
            try:

                if instanceType != 'all':
                    if not acceptInstance(instance):
                        continue

                instancepath = os.path.join(root, instance)
                print("processing instance " + instance)

                if solverType == "ILP":
                    solveInstanceWithILP(instancepath)
                elif solverType in ["greedy", "grasp", "brkga"]:
                    grasp.run(instancepath, solverType)

            except Exception:
                all_ok = False
                print("Exception in user code:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
        
                
