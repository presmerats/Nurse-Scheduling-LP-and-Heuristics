# AMMM-Project

## Folders

+ Instances
    ** Final
        - MediumSet
            + folder that saves the small-medium set of instances (~10 and that take 30~60 minutes to solve by ILP)
        - LargeSet
            + folder that saves all the instances ever created , comprehends instances that take more than 60min to solve, and are around 100
    * Pending
        - used to store instances that need to be tested somehow separated from the Medium and Large set
    * Pending2, Paused, 
        - similar than Pending
    * Test
        - instances used to test the validity of the models
+ Results
    * Final 
        - LargeSet
        - MediumSet
        - ILPEvolution
        - GRASPvsBRKGA
    * Pending
    * Test


## Running 

### launcher

To solve instances of the problem with the models run, from ./Tools/Launcher:

For ILP (calls oplrun from commandline)
`
python launcher.py --solver ILP
`

For GRASP
`
python launcher.py --solver grasp
`
For BRKGA

`
python launcher.py --solver brkga
`

These commands solve all instances from the default folder ./Instances/Pending and save the results in a json format to ./Results/Pending 
Options:

Instances folder and results folder (paths must be relative to ./Tools/Launcher)
:
`
python launcher.py --solver grasp --instances ../../Instances/Final/MediumSet --results ../../Results/Final/MediumSet
`


GRASP parameters:
`
python launcher.py --solver grasp --iterations 5 --alpha 0.15 --ls best
`

BRKGA parameters:
`
python launcher.py --solver brkga --generations 1 --eliteprop 0.3 --mutantprop 0.2 --population 2 --inheritance 0.1
`


### Other options

Other options that can be used are to use the ./Metaheuristics/main.py file from it's 'main' section, calling any of the "entry points" of the Metaheuristics algorithms.


## Reporting

mediumSetGraph.py, takes all json files in a folder and creates 2 graphs, one comparing the solving times for differents instances for the 3 algorithms (ILP, GRASP and BRKGA). It expects to find json files with results from executions of the 3 algorithms in the indicated folder:
`
python mediumSetGraph.py ../../Results/MediumSet
`


summary_of_executions.py, example file that reads json results files from a folder and plots all the resutls in a graph


classifider.py script used to organize the executions of instances by the ILP, it saves the instances files (.dat) to the Instances/Final/ with a name that reflects the time it takes for the ILP to solve it.

