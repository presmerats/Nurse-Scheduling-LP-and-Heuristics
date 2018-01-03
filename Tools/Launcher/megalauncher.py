
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

    with open(os.path.join(folder,filename), 'r') as f:
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
        filename='done_alphas.txt',
        listname="alphas",
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
        filename='done_maxiters.txt',
        listname="maxiters",
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
        filename='done_lstypes.txt',
        listname="lstypes",
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
        filename='done_lsiterations.txt',
        listname="lsiterations",
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
        filename='done_generations.txt',
        listname="generations",
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
        filename='done_eliteprops.txt',
        listname="eliteprops",
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
        filename='done_mutantprops.txt',
        listname="mutantprops",
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
        filename='done_inheritances.txt',
        listname="inheritances",
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
        filename='done_populations.txt',
        listname="populations",
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


def done(instance, status_list, param, paramvalue = None):

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
        param_value)

    """
        results folders:
        Results
            Final
                LargeSet
                    alpha
                    maxiter
                    ...

    """
    
    resultsfolder = os.path.join(
        '../../Results/Final/LargeSet',
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

    runInstance(
        instancepath=instance,
        results_folder=resultsfolder,
        instanceType='all',
        solverType=solver,
        args=args
        )
    


def update_partial_results_lists(
    progress_files_folder,
    instance,
    "alphas",
    alpha):
    pass


def update_results_list(
    progress_files_folder,
    instance,
    "alphas"):
    pass




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "folder",
        help="instances folder where to read instances files from")
    args = parser.parse_args()
    instances_folder = args.folder

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
    inheritances = range(0, 1, 0.1)
    populations = range(1,6)
    decoder = "hexcess"



    os.chdir(instances_folder)
    for root, dirs, files in os.walk("."):
        all_ok = True
        for inst in files:
            try:

                instance = os.path.join(root,inst)

                status_list = update_instance_list(progress_files_folder)
                if not done(instance, status_list, "alphas"):
                    for alpha in alphas:
                        if not done(instance, status_list, "current_alpha", alpha):
                            success = makeRunInstance(
                                instance=instance,
                                solver="grasp",
                                params=basic_params_grasp,
                                selected_param="alpha",
                                param_value=alpha
                                )
                            if success:
                                # updates done_current_alpha.txt 
                                # -> has current instance and done alphas
                                update_partial_results_lists(
                                    progress_files_folder,
                                    instance,
                                    "alphas",
                                    alpha)

                    # updates done_alphas.txt
                    # -> has each instance done with all alphas
                    update_results_list(
                        progress_files_folder,
                        instance,
                        "alphas")

            except Exception:
                all_ok = False
                print("Exception in user code:")
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
