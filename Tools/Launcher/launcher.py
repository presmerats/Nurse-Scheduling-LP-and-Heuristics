"""
    this script 
        1- takes instances from ../../Instances/Pending
    and then for each instance:
        2- prepares a .mod file that executes the instance and writes to a log file in ../../Results/Pending/log-<instance>.json
        3- that .mod file must save a key value "solver" : "ILP" inside the written json file
    executes
        4- executes in shell the command "oplrun -v <name>.mod" with the env var LD_LIBRARY_PATH=/opt/ibm/ILOG/CPLEX_Studio126/opl/bin/x86-64_linux

"""

import json
import sys
import os
import traceback
import shutil
import re
from subprocess import call,check_call, Popen, PIPE
from pathlib import Path, PurePath
import argparse

parentPath = os.path.abspath(os.path.join("..","..","Metaheuristics","GRASP"))
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
parentPath = os.path.abspath(os.path.join("..","..","Metaheuristics","BRKGA"))
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
parentPath = os.path.abspath(os.path.join("..","..","Metaheuristics"))
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from Greedy import *
from LocalSearch import *
from BRKGA_main import *
from Grasp import *
import main as metaheuristics

mod_header_template = os.path.abspath(os.path.join('..','Instance_Generator','Complex Generator','Test-header2.template'))
mod_footer_template = os.path.abspath(os.path.join('..','Instance_Generator','Complex Generator','Test-footer.template'))


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


def prepareModFile(instancepath, resultspath, tilim=4200.0, path=Path(), gap=None):
    print("preparing mod file for :" + instancepath)

    filename = '../../Tools/Launcher/temp.mod'
    filename = PurePath(path, filename)

    modelfile = '../../ILP/model01.mod'
    modelfile = os.path.abspath(modelfile)

    logfile = os.path.splitext(os.path.basename(instancepath))[0] + '.json'
    logname = '../../Results/Pending/' + logfile
    if os.path.exists(resultspath):
        logname = os.path.join(resultspath, logfile)


    with open(filename, 'w') as f:

        with open(mod_header_template, 'r') as h:
            for line in h:
                if "model01-hfree.mod" in line:
                    line = line.replace("model01-hfree.mod", str(modelfile))

                if line.startswith("var logname = \""):
                    line = "var logname = \"" + logname + "\";\n"

                if gap is not None and line.startswith(" //cplex.epgap=0.01;"):
                    line = " cplex.epgap=" + str(gap) + ";\n"
                    print("")
                    print(" writing gap!")
                    print(line)
                    print("")

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


def solveInstanceWithILP(instancepath, resultspath=None, tilim=4200.0,  gap=None):

    tilim2 = 4200.0
    if tilim is not None:
        tilim2 = tilim

    modfile = prepareModFile(instancepath=instancepath, resultspath=resultspath, tilim=tilim2, gap=gap)

    print("solving instance " + modfile)
    output, error = shellexec("oplrun -v " + modfile)
    print("output = ")
    print(output)

    # append output to results file
    with open(os.path.join(resultspath, os.path.basename(instancepath) + ".log" ), 'w+' ) as flog:
        flog.write(output.decode("utf-8"))


def acceptInstance(instance):

    i1 = instance.find('-')
    time_it_takes_to_solve = -1
    try:
        time_it_takes_to_solve = int(instance[:i1])
    except:
        time_it_takes_to_solve = sys.maxsize

    return time_it_takes_to_solve < 3




def runInstance(instancepath,
                 results_folder,
                 instanceType,
                 solverType,
                 args):

    if not os.path.exists(instancepath):
        return False

    try:

        if instanceType != 'all':
            if not acceptInstance(instance):
                return False
            
        if solverType not in ('ILP', 'grasp', 'brkga'):
            print('You need to define a solving method: grasp or brkga')
            sys.exit(1)

        print("Processing instance: " + instancepath)

        if solverType == "ILP":
            solveInstanceWithILP(instancepath, results_folder, args.tilim, args.gap)
        elif solverType == "grasp":
            metaheuristics.run(instancepath=instancepath,
                solverType=solverType,
                results_path=results_folder,
                grasp_alpha=args.alpha,
                grasp_iterations=args.iterations,
                grasp_lstype=args.ls,
                grasp_lsiterations=args.lsiterations
                )
        elif solverType == "brkga":
            metaheuristics.run(instancepath=instancepath,
                solverType=solverType,
                results_path=results_folder,
                brkga_generations=args.generations,
                brkga_eliteprop=args.eliteprop,
                brkga_mutantprop=args.mutantprop,
                brkga_population=args.population,
                brkga_inheritance=args.inheritance,
                brkga_decoder=args.decoder
                )

        return True

    except Exception:
        all_ok = False
        print("Exception in user code:")
        print("-"*60)
        traceback.print_exc(file=sys.stdout)
        print("-"*60)

        return False



def runInstances(instances_folder,
                 results_folder,
                 instanceType,
                 solverType,
                 args):

    if not os.path.exists(instances_folder):
        print("check folder paths!")
        exit()

    #os.chdir(instances_folder)
    for root, dirs, files in os.walk(os.path.abspath(instances_folder)):
        all_ok = True
        if root.find("maxPresence")== -1:
            continue
        for instance in files:
            try:

                if instanceType != 'all':
                    if not acceptInstance(instance):
                        continue
                    
                if solverType not in ('ILP', 'grasp', 'brkga'):
                    print('You need to define a solving method: grasp or brkga')
                    sys.exit(1)

                instancepath = os.path.join(root, instance)
                print("Processing instance: " + instance)

                if solverType == "ILP":
                    solveInstanceWithILP(instancepath, results_folder, args.tilim, args.gap)
                elif solverType == "grasp":
                    metaheuristics.run(instancepath=instancepath,
                        solverType=solverType,
                        results_path=results_folder,
                        grasp_alpha=args.alpha,
                        grasp_iterations=args.iterations,
                        grasp_lstype=args.ls,
                        grasp_lsiterations=args.lsiterations
                        )
                elif solverType == "brkga":
                    metaheuristics.run(instancepath=instancepath,
                        solverType=solverType,
                        results_path=results_folder,
                        brkga_generations=args.generations,
                        brkga_eliteprop=args.eliteprop,
                        brkga_mutantprop=args.mutantprop,
                        brkga_population=args.population,
                        brkga_inheritance=args.inheritance,
                        brkga_decoder=args.decoder
                        )

            except Exception:
                all_ok = False
                print("Exception in user code:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60)
        


if __name__ == '__main__':

    # set instances folder
    # set results folder
    # set model params (alpha_grasp, num-iterations, inheritance, num pop, num generations, num mutatns)


    parser = argparse.ArgumentParser()
    parser.add_argument("--solver",help="solver model/algorithm to use [ILP, grasp, brkga]")
    parser.add_argument("--instances",help="instances folder where to read instances files from")
    parser.add_argument("--results",help="results folder where to save result files to")
    parser.add_argument("--type",help="instance type, selects instances by timelimit")

    parser.add_argument("--gap",help="ILP solver gap", type=float)
    parser.add_argument("--tilim",help="ILP solver gap", type=float)

    parser.add_argument("--alpha",help="grasp alpha param", type=float)
    parser.add_argument("--iterations",help="grasp num iterations param", type=int)
    parser.add_argument("--ls",help="values first or best (improvement)")
    parser.add_argument("--lsiterations",help="grasp final LS iterations param", type=int)

    parser.add_argument("--generations",help="brkga num generations", type=int)
    parser.add_argument("--eliteprop",help="brkga elite proportion", type=float)
    parser.add_argument("--mutantprop",help="brkga mutant proportion", type=float)
    parser.add_argument("--population",help="brkga population size", type=int)
    parser.add_argument("--inheritance",help="brkga inheritance probability", type=float)
    parser.add_argument("--decoder",help="decoder type=[horder, hini, hexcess]")

    args = parser.parse_args()

    solverType = "ILP"
    if args.solver:
        solverType = args.solver

    instanceType = 'all'
    if args.type:
        instanceType = args.type

    instances_folder = os.path.join('..','..','Instances','Pending')
    if args.instances:
        instances_folder = args.instances

    results_folder = os.path.join('..','..','Results','Pending')
    if args.results:
        results_folder = args.results

    if not os.path.exists(instances_folder):
        print("check folder paths!")
        exit()


    runInstances(
        instances_folder,
        results_folder,
        instanceType,
        solverType,
        args
        )


    