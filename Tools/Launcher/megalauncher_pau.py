
"""

Goal:
    -execute instances of the largeset with different parameters

Strategy:
    -the strategy is to compute all parameter values for each instance
    before going to another instance or another parameter
    -the list of instances, parameters and values already execute will be
    saved in plain text files as lists, in order to be able to stop and
    continue later with the executions


Pseudocode
alphas=[],maxiters=[],generations=[],...
basic_params_grasp={}
basic_params_brkga=[]

for instance in largeset

    update_results_list # reads list files from disk

    if not done(instance, "alpha"):
        for alpha in alphas:
            execute(basic_params_grasp,alpha,"alphas")
            update_partial_results_lists("alphas",alpha)
            # updates done_alphai.txt -> has current instance and done alphas

        update_results_list("alphas",instance)
        # updates done_alphas.txt -> has each instance done with all alphas

    if not done(instance, "maxiter"):
        for maxiter in maxiters:
            execute(basic_params_grasp,maxiter,"maxiters")
            update_partial_results_lists("maxiter",maxiter)
            # updates done_alphai.txt -> has current instance and done alphas

        update_results_list("maxiters",instance)
        # updates done_alphas.txt -> has each instance done with all alphas

"""


import json
import sys
import os
import traceback
import shutil
import re
from pathlib import Path, PurePath
import argparse
import time
from launcher import *

demo = True

                

class Execution:
    def __init__(
        self,
        grasp_alpha=None,
        grasp_iterations=None,
        grasp_lstype=None,
        grasp_lsiterations=None,
        brkga_generations=None,
        brkga_eliteprop=None,
        brkga_mutantprop=None,
        brkga_population=None,
        brkga_inheritance=None,
        brkga_decoder=None
        ):

        self.alpha = grasp_alpha
        self.iterations = grasp_iterations
        self.ls = grasp_lstype
        self.lsiterations = grasp_lsiterations
        self.generations = brkga_generations
        self.eliteprop = brkga_eliteprop
        self.mutantprop = brkga_mutantprop
        self.population = brkga_population
        self.inheritance = brkga_inheritance
        self.decoder = brkga_decoder







def update_instance_list_aux(folder, filename, listname, status_list, listtype):

    status_list[listname] = []
    
    try:
        with open(os.path.join(folder,filename), 'r+') as f:
            current_list = []

            for line in f:
                if line.endswith('\n'):
                    line = line[:-1]
                if listtype == "list":
                    current_list.append(line)
                elif listtype == "dict":
                    linesplit = line.split(",")
                    current_list.append([linesplit[0], linesplit[1]]) 

            status_list[listname] = current_list
    except:
        pass

 

def update_instance_list(folder):
    """
        status files:
            done_alphas.txt :
                instance_path1
                instance_path2
                ...

            done_alpha_current_instance.txt
                instance_path1 , alpha1
                instance_path1 , alpha2

            similar for other params

        status_list:
            {
            'alphas': [instance_path1, instance_path2,...]
            'current_alpha': [ {'instance': 'paramvalue'},...]
            [instance_path1, instance_path2,...]
            'current_alpha': [ {'instance': 'paramvalue'},...]

            }

    """
    status_list = {}

    update_instance_list_aux(
        folder=folder,
        filename='done_alpha.txt',
        listname="alpha",
        status_list=status_list,
        listtype="list"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_alpha_current_instance.txt',
        listname="current_alpha",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_maxiter.txt',
        listname="maxiter",
        status_list=status_list,
        listtype="list"
        )
    update_instance_list_aux(
        folder=folder,
        filename='done_maxiter_current_instance.txt',
        listname="current_maxiter",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_lstype.txt',
        listname="lstype",
        status_list=status_list,
        listtype="list"
        )
    update_instance_list_aux(
        folder=folder,
        filename='done_lstype_current_instance.txt',
        listname="current_lstype",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_lsiteration.txt',
        listname="lsiteration",
        status_list=status_list,
        listtype="list"
        )
    update_instance_list_aux(
        folder=folder,
        filename='done_lstireation_current_instance.txt',
        listname="current_lsiteration",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_generation.txt',
        listname="generation",
        status_list=status_list,
        listtype="list"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_generation_current_instance.txt',
        listname="current_generation",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_eliteprop.txt',
        listname="eliteprop",
        status_list=status_list,
        listtype="list"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_eliteprop_current_instance.txt',
        listname="current_eliteprop",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_mutantprop.txt',
        listname="mutantprop",
        status_list=status_list,
        listtype="list"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_mutantprop_current_instance.txt',
        listname="current_mutantprop",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_inheritance.txt',
        listname="inheritance",
        status_list=status_list,
        listtype="list"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_inheritance_current_instance.txt',
        listname="current_inheritance",
        status_list=status_list,
        listtype="dict"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_population.txt',
        listname="population",
        status_list=status_list,
        listtype="list"
        )

    update_instance_list_aux(
        folder=folder,
        filename='done_population_current_instance.txt',
        listname="current_population",
        status_list=status_list,
        listtype="dict"
        )

    return status_list


def done(instance, status_list, param, paramvalue=None):

    if paramvalue is None:

        return instance in status_list[param]
    else:
        for elemdone in status_list[param]:
            if elemdone[0] == instance and elemdone[1] == paramvalue:
                return True
        return False

    


def makeRunInstance(instance,
        solver,
        params,
        selected_param,
        param_value):

    """
        results folders:
        Results
            Final
                LargeSet
                    alpha
                    maxiter
                    ...

    """
    global demo 
    if demo:
        time.sleep(0.5)
        return True


    resultsfolder = os.path.join(
        '../../Results/Final/LargeSet_20180103',
        selected_param)

    # parameteres
    params[selected_param] = param_value
    if solver == "grasp":
        args = Execution(
            grasp_alpha=params["alpha"],
            grasp_iterations=params["maxiter"],
            grasp_lstype=params["lstype"],
            grasp_lsiterations=params["lsiterations"],
            brkga_generations=None,
            brkga_eliteprop=None,
            brkga_mutantprop=None,
            brkga_population=None,
            brkga_inheritance=None,
            brkga_decoder=None)

    else:
        args = Execution(
            grasp_alpha=params["alpha"],
            grasp_iterations=params["maxiter"],
            grasp_lstype=params["lstype"],
            grasp_lsiterations=params["lsiterations"],
            brkga_generations=None,
            brkga_eliteprop=None,
            brkga_mutantprop=None,
            brkga_population=None,
            brkga_inheritance=None,
            brkga_decoder=None)

    return runInstance(
        instancepath=instance,
        results_folder=resultsfolder,
        instanceType='all',
        solverType=solver,
        args=args
        )


def update_partial_results_lists(
    progress_files_folder,
    instance,
    parameter,
    alpha):

    """
        done_alpha_current_instance.txt
                instance_path1 , alpha1
                instance_path1 , alpha2


        update_instance_list_aux(
            folder=folder,
            filename='done_alpha_current_instance.txt',
            listname="current_alpha",
            status_list=status_list,
            listtype="dict"
            )
    """

    filename = "done_" + str(parameter)  + "_current_instance.txt"
    with open(os.path.join(progress_files_folder, filename), 'a+') as f:
        f.write(instance + "," + str(alpha) + "\n")



def update_results_list(
    progress_files_folder,
    instance,
    parameter):
    
    # update progress list

    filename = "done_" + str(parameter)  + ".txt"
    with open(os.path.join(progress_files_folder, filename), 'a+') as f:
        f.write(instance + "\n")

    # wipe current instance progress list
    filename = "done_" + str(parameter)  + "_current_instance.txt"
    with open(os.path.join(progress_files_folder, filename), 'w+') as f:
        f.write("")


def parameter_executions_loop(
    instance,
    status_list,
    parameter_name,
    parameter_values_list,
    parameter_solver,
    solver_basic_params,
    progress_files_folder):

    if not done(instance, status_list, parameter_name):
        for param_value in parameter_values_list:
            if not done(instance, status_list, "current_" + str(parameter_name), param_value):
                success = makeRunInstance(
                    instance=instance,
                    solver=parameter_solver,
                    params=solver_basic_params,
                    selected_param=parameter_name,
                    param_value=param_value
                )
                if success:
                    # updates done_current_alpha.txt
                    # -> has current instance and done alphas
                    update_partial_results_lists(
                        progress_files_folder,
                        instance,
                        parameter_name,
                        param_value)
                else:
                    print("Error running " + str(instance) +
                          " for param " + parameter_name +
                          "=" + str(param_value) +
                          " solver " + str(parameter_solver))

        # updates done_alphas.txt
        # -> has each instance done with all alphas
        update_results_list(
            progress_files_folder,
            instance,
            parameter_name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder",
        help="instances folder where to read instances files from")
    parser.add_argument(
        "--demo",
        help="demo mode", action='store_true')
    args = parser.parse_args()
    instances_folder = args.folder


    demo = args.demo

    if not os.path.exists(instances_folder):
        print("check folder paths!")
        exit()


    progress_files_folder = '../../Results/Progress'


    basic_params_grasp ={
        'alpha': '0.2',
        'maxiter': 3,
        'lstype': 'first',
        'lsiterations': 5
    }
    alphas = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9]
    maxiters = range(1,10)
    lstypes = "first"
    lsiterations = range(1,5)

    basic_params_brkga ={
        'generations': 3,
        'eliteprop': 0.3,
        'mutantprop': 0.1,
        'population': 3,
        'inheritance': 0.7,
        'decoder': 'hexcess'
    }
    generations = range(1,10)
    eliteprops = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9]
    mutantprops = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9]
    inheritances = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9]
    populations = range(1,6)
    decoder = "hexcess"



    os.chdir(instances_folder)
    for root, dirs, files in os.walk("."):
        all_ok = True
        for inst in files:
            try:

                instance = os.path.join(root,inst)
                status_list = update_instance_list(progress_files_folder)

                # parameter_executions_loop(
                #     instance,
                #     status_list,
                #     parameter_name="alpha",
                #     parameter_values_list=alphas,
                #     parameter_solver="grasp",
                #     solver_basic_params=basic_params_grasp,
                #     progress_files_folder=progress_files_folder)

                parameter_executions_loop(
                    instance,
                    status_list,
                    parameter_name="maxiter",
                    parameter_values_list=maxiters,
                    parameter_solver="grasp",
                    solver_basic_params=basic_params_grasp,
                    progress_files_folder=progress_files_folder)

                # parameter_executions_loop(
                #     instance,
                #     status_list,
                #     parameter_name="lsiteration",
                #     parameter_values_list=lsiterations,
                #     parameter_solver="grasp",
                #     solver_basic_params=basic_params_grasp,
                #     progress_files_folder=progress_files_folder)

                # parameter_executions_loop(
                #     instance,
                #     status_list,
                #     parameter_name="generation",
                #     parameter_values_list=generations,
                #     parameter_solver="brkga",
                #     solver_basic_params=basic_params_brkga,
                #     progress_files_folder=progress_files_folder)


                # parameter_executions_loop(
                #     instance,
                #     status_list,
                #     parameter_name="eliteprop",
                #     parameter_values_list=eliteprops,
                #     parameter_solver="brkga",
                #     solver_basic_params=basic_params_brkga,
                #     progress_files_folder=progress_files_folder)


                parameter_executions_loop(
                    instance,
                    status_list,
                    parameter_name="mutantprop",
                    parameter_values_list=mutantprops,
                    parameter_solver="brkga",
                    solver_basic_params=basic_params_brkga,
                    progress_files_folder=progress_files_folder)


                parameter_executions_loop(
                    instance,
                    status_list,
                    parameter_name="inheritance",
                    parameter_values_list=inheritances,
                    parameter_solver="brkga",
                    solver_basic_params=basic_params_brkga,
                    progress_files_folder=progress_files_folder)


                parameter_executions_loop(
                    instance,
                    status_list,
                    parameter_name="population",
                    parameter_values_list=populations,
                    parameter_solver="brkga",
                    solver_basic_params=basic_params_brkga,
                    progress_files_folder=progress_files_folder)


            except Exception:
                all_ok = False
                print("Exception in user code:")
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
