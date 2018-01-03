
import json
import sys
import os
from random import randrange
import argparse
import traceback
from datetime import datetime

parentPath = os.path.abspath("../../Metaheuristics")
print(parentPath)
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
from Common.NurseSchedulingProblem import *

try:
  basestring
except NameError:
  basestring = str



def checkResult(key, v):
    """ 
        check validity (constrains) for each schedule
        check feasibility (demand for each hour)
        status = isFeasible() and totallyValid()
        return filename and status

    """

    # extract file name = key
    filename = key

    solkey = "solution"
    if "Solution" in v.keys():
        solkey = "Solution"
    elif solkey not in v.keys():
        return filename, "Unsolved"


    datakey = "data"
    if "Data" in v.keys():
        datakey = "Data"

    # check validity
    valid = False
    if isinstance(v[solkey], basestring):
        valid = True
    else:
        valid = complete_solution_validation(v[datakey], v[solkey])

    # check feasibility
    feasible = False
    if isinstance(v[solkey], basestring) and v[solkey].find("(optimal)") > -1:
        feasible = True
    elif isinstance(v[solkey], dict):
        feasible = isFeasible(v[solkey], v[datakey])

    return filename, valid & feasible


def writeResult(filename, name, status, filepath):

    with open(filepath, 'a+') as f:
        f.write(filename + ", " + name + ", " + str(status) + "\n")


def initResultsFile():

    filepath = os.path.abspath('../../Results/check/checked_list' +
          '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) +
          '.csv')

    with open(filepath, 'w+') as f:
        f.write("")

    return filepath

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("folder",help="folder where to gather results from")
    args = parser.parse_args()

    check_filepath = initResultsFile()

    os.chdir(args.folder)
    for root, dirs, files in os.walk("."):
        results = []
        for filename in files:
            try:

                filepath = os.path.join(root,filename)
                log = json.load(open(filepath))

                for elem in log:

                    try:
                        for k,v in elem.items():
                            
                            if k == "end":
                                continue
                            name, status = checkResult(k, v)
                            writeResult(filepath, name, status, check_filepath)

                    except Exception:
                        print("Exception in element:")
                        print("-"*60)
                        traceback.print_exc(file=sys.stdout)
                        print("")
                        print(filepath)
                        print(v.keys())
                        print("-"*60)

            except Exception:
                print("Exception in element:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print(filename)
                print("-"*60)   
            
