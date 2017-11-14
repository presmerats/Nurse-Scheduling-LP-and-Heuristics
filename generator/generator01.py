import numpy as np
from random import randrange
import pprint
from datetime import datetime
#import matplotlib.pyplot as plt

import os, sys


def write(instance, instance_type=""):
    
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(instance)

    filename = 'instance-' +instance_type+ '-' + str(instance["nNurses"]) +'-' + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) + '.dat' 
    with open(filename,'w') as f:

        f.write('/*********************************************\n')
        f.write(' * OPL 12.6.0.0 Data\n')
        f.write(' * Author: Adrian Rodriguez Bazaga, Pau Rodriguez Esmerats\n')
        f.write(' * Creation Date: ' + '{0:%d/%m/%Y at %H:%M:%S}'.format(datetime.now()) + '\n')
        f.write(' *********************************************/\n\n')

        for k,v in instance.items():
            if k in ["demand","demandh_raw"]:
                f.write(k+'= [')
                for item in v:
                    f.write(str(item) + " ")
                f.write(' ];\n')
            else:
                f.write(k + '=' + str(v) +';\n')
        f.close()


def writeTestModel(dat_files_folder='.'):

    filename = 'Test-'  + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) + '.mod' 
    with open(filename,'w') as f:

        with open('Test-header.template','r') as h:
            for line in h:
                f.write(line)


        # walk dir for .dat files
        dirs = os.listdir( dat_files_folder )


        # for each of the files write a line like this one
        for file in dirs:
            if file.endswith('.dat'):
                f.write('myTest(def, cplex,"' + file +'","SUCCESS" );\n')

        with open('Test-footer.template','r') as h:
            for line in h:
                f.write(line)

    # Pending create folder and move model and dat files there, to ease the import to cplex

def generate2(i):


    # parameteres definition

    # constraints parameters
    maxConsec_base = 4
    maxConsec_variability = 8
    maxPresence_base = 10
    maxPresence_base_variability = 4
    maxHours_base  = 10
    maxHours_base_variability = 2
    minHours_base = 1
    minHours_base_variability = maxHours_base/2
    nNurses = i


    #max number of demand must be nNurses/each hour so 24*nNurses in total
    #generate a proportion between the 3 distributions
    p1 = randrange(24)
    proportion1=24/3
    proportion2=24/3
    proportion3=24/3
    base= nNurses/3
    if p1>12:
        p2 = randrange(p1)
        proportion1=int(p2*base)
        proportion2=int((p1-p2)*base)
        proportion3=int((24-p1)*base)
    else:
        p2 = randrange(p1,24)
        proportion1=int(p1*base)
        proportion2=int((p2-p1)*base)
        proportion3=int((24-p2)*base)

    

    # distributions
    n1_mu=8
    n1_sigma=5
    u1_a=10
    u1_b=17
    n2_mu=20
    n2_sigma=10



    # final computations

    instance={}
    instance["nNurses"] = nNurses
    instance["maxConsec"] = maxConsec_base + randrange(maxConsec_variability)
    instance["maxPresence"] = maxPresence_base + randrange(maxPresence_base_variability)
    instance["maxHours"] = maxHours_base + randrange(maxHours_base_variability)
    instance["minHours"] = minHours_base + randrange(int(minHours_base_variability))

    # lower normal distribution
    demand_samples = [int(abs(x)) for x in np.random.normal(n1_mu, n1_sigma, proportion1) ]
    
    # uniform distribution
    demand_samples2 = \
        [ int(abs(x)) for x in np.random.uniform(u1_a,u1_b, proportion2) ]

    # upper normal distribution distributions
    demand_samples3 = \
        [int(abs(x)) for x in np.random.normal(n2_mu, n2_sigma, proportion3) ]




    # get the histogram and save it as demandh
    demand_samples.extend(demand_samples2)
    demand_samples.extend(demand_samples3)
    
    hist, edges = np.histogram(
        demand_samples,
        bins=24, 
        range=(1,24), 
        density=False)
    #instance["demandh_raw"] = hist 
    instance["demand"] = [ x if x < (nNurses+1) else nNurses for x in hist ]

    return instance


def gen3Concentrated(start, maxConsec, maxHours, maxPresence):

    # init w
    w = [ 0 for i in range(1,25) ]
    #print(w)

    # choose a start point
    i = start

    # put maxConsec+rest+maxConsec until maxHours or maxPresence is over
    while ( i<= 24 and  maxHours >0 and maxPresence>0):
        
        # work hours
        maxConsecSave=maxConsec
        while(i<=24 and maxConsec>0):
            w[i-1] = 1
            maxConsec -=1
            maxHours -=1
            maxPresence -=1
            i+=1

        #print(w)
        #print(i)

        # rest
        if(i<=24):
            w[i-1]=0
            maxPresence -=1
            i+=1
            maxConsec=maxConsecSave

    #print(w)
    return w

def gen3Sparse(start,maxConsec, maxHours, maxPresence):

    # init w
    w = [ 0 for i in range(1,25) ]
    #print(w)

    # choose a start point
    i = start

    # put 1hour+rest until maxPresence or maxHours
    while ( i<= 24 and  maxHours >0 and maxPresence>0):
        
        # work hours
        maxConsecSave=maxConsec
        if(i<=24 and maxConsec>0):
            w[i-1] = 1
            maxConsec -=1
            maxHours -=1
            maxPresence -=1
            i+=1

        # rest
        if(i<=24):
            w[i-1]=0
            maxPresence -=1
            i+=1
            maxConsec=maxConsecSave

    #print(w)
    return w


def generate3(nNurses):

    # constraints parameters
    maxConsec_base = 2
    maxConsec_variability = 8
    maxPresence_base = 7
    maxPresence_base_variability = 4
    maxHours_base  = 5
    maxHours_base_variability = 2
    minHours_base = 1
    minHours_base_variability = maxHours_base/2
    
    instance={}
    instance["nNurses"] = nNurses
    instance["maxConsec"] = maxConsec_base + randrange(maxConsec_variability)
    instance["maxPresence"] = maxPresence_base + randrange(maxPresence_base_variability)
    instance["maxHours"] = maxHours_base + randrange(maxHours_base_variability)
    instance["minHours"] = minHours_base + randrange(int(minHours_base_variability))

    instance["nNurses"] = nNurses
    instance["maxConsec"] = maxConsec_base 
    instance["maxPresence"] = maxPresence_base 
    instance["maxHours"] = maxHours_base 
    instance["minHours"] = minHours_base 


    # init demand
    demand = [ 0 for i in range(1,24+1) ]

    # init w matrix
    w=[]

    for i in range(0,nNurses):
        
        # select the type
        select = randrange(10)

        if select<5:
            # generate concentrated schedule
            start=2+randrange(4)-2 
            w.append(
                gen3Concentrated(start=start, 
                    maxConsec=instance["maxConsec"],
                    maxHours=instance["maxHours"],
                    maxPresence=instance["maxPresence"])
                )

        elif select<9:
            # generate concentrated schedule
            start=22+randrange(2)-1 
            w.append(
                gen3Concentrated(start=start, 
                    maxConsec=instance["maxConsec"],
                    maxHours=instance["maxHours"],
                    maxPresence=instance["maxPresence"])
                )
        else:
            # generate sparse schedule
            start=12+randrange(8)-4
            w.append(gen3Sparse(start=start, 
                    maxConsec=instance["maxConsec"],
                    maxHours=instance["maxHours"],
                    maxPresence=instance["maxPresence"])
                )

    
    # mix
    for i in range(0,len(w)):
        print(w[i])
        for j in range(1,24+1):
            demand[j-1]+=w[i][j-1]


    print("")
    print(demand)
    instance["demand"] = demand
    return instance



if __name__ == '__main__':

    #instances = generate2(100)
    #write(instances,"distr")

    instances = generate3(100)
    write(instances,"manual")

    writeTestModel()