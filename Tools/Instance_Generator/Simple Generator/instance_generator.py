'''
AMMM project
Instance Generator

Adrian Rodriguez Bazaga (adrianrodriguezbazaga@gmail.com)
Pau Rodriguez Esmerats (rodriguez.pau@gmail.com)
'''

import sys
import random
import time
import numpy as np
from scipy.stats import truncnorm
import pprint

RAND_SEED=int(time.time())

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)
    
def generateRandomDemandArray(hoursPerDay, numNurses):
    random.seed(RAND_SEED)
    demand_h_tmp = []
    RNG = get_truncated_normal(mean=numNurses-1, sd=numNurses/2, low=0, upp=numNurses-1)
    
    for i in range(hoursPerDay):
        number = RNG.rvs()
        demand_h_tmp.append(int(number))
        
    return demand_h_tmp

def main(argc, argv):
    if argc != 7:
        print("Error providing the instance generator parameters, use the following format:")
        print("./{0} <hours_per_day> <num_nurses> <min_hours> <max_hours> <max_consec> <max_presence>" % format(argv[0]))
        return(0)
        
    # Parsing params
    hoursPerDay = int(argv[1])
    numNurses = int(argv[2])
    minHours = int(argv[3])
    maxHours = int(argv[4])
    maxConsec = int(argv[5])
    maxPresence = int(argv[6])
    
    # Generating the demand-per-hour array
    demand_h = generateRandomDemandArray(hoursPerDay, numNurses)

    # Writting the instance into a file
    
    filename = "./instance_{0}_{1}.dat".format(numNurses, RAND_SEED)
    output_file = open(filename, "w")
    
    pp = pprint.PrettyPrinter(indent=4, depth=200, stream=output_file)
    
    output_file.write("nNurses={0};\n".format(numNurses))
    output_file.write("minHours={0};\n".format(minHours))
    output_file.write("maxHours={0};\n".format(maxHours))
    output_file.write("maxConsec={0};\n".format(maxConsec))
    output_file.write("maxPresence={0};\n".format(maxPresence))
    output_file.write("demand=[{0}];".format(' '.join([str(x) for x in demand_h]))); 
    
    output_file.close()
    
    print ("The instance has been successfully dumped into '{0}'".format(filename))

if __name__== "__main__":
	main(len(sys.argv), sys.argv)