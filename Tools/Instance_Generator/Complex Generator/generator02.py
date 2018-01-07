import numpy as np
import math
from random import randrange
import pprint
from datetime import datetime
from pathlib import Path, PurePath
#import matplotlib.pyplot as plt

import os, sys


import re


def sort_nicely( l, reverse=False ):
    """ Sort the given list in the way that humans expect.
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    l.sort( key=alphanum_key, reverse=reverse )





def write(instance, instance_type="", path='.'):
    
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(instance)

    # i-percentage-nNurses-nlimit-date.dat
    filename = 'i-' + \
        instance_type + '-' + \
        str(instance["surplus"]) +'-' + \
        str(int(instance["nNurses"])) +'-' + \
        str(instance["nNurses-limit"]) +'-' + \
        str(instance["hours"]) +'h-' + \
        str(instance["maxPresence"]) +'mxP-' + \
        str(instance["maxConsec"]) +'mxC-' + \
        str(instance["maxHours"]) +'mxH-' + \
        str(instance["minHours"]) +'mnH-' + \
        str(instance["centroides"])+'Cnt-' + \
        '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) + \
        str(randrange(1000)) + '.dat' 
    filename = PurePath(path, filename)
    filename = str(filename)

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
            elif k in ["nNurses-limit","surplus"]:
                continue
            elif k in ["centroides"]:
                continue
            else:
                f.write(k + '=' + str(v) +';\n')
        f.close()


def writeTestModel(path=Path()):

    filename = 'Test-' \
        + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) + '.mod'
        
    filename = PurePath(path,filename)
    with open(filename,'w') as f:

        with open('Test-header.template','r') as h:
            for line in h:
                f.write(line)


        # walk dir for .dat files
        dirs = os.listdir( str(PurePath(path)) )
        # sort files
        sort_nicely(dirs, reverse=True)



        # objective function expected value (should be extracted from filename)
        expected = 1
        # for each of the files write a line like this one
        for file in dirs:
            if file.endswith('.dat'):
                # f.write('var src = new IloOplModelSource("model01.mod");\n')
                # f.write('var def = new IloOplModelDefinition(src);\n')
                # f.write('var cplex = new IloCplex();\n')

                f.write('myTest(def, cplex,"' + file +'", logname, tilim,  "SUCCESS", '+str(expected)+' );\n')

                # f.write('def.end();\n')
                # f.write('cplex.end();\n')
                # f.write('src.end();\n\n')

        with open('Test-footer.template','r') as h:
            for line in h:
                f.write(line)

    # Pending create folder and move model and dat files there, to ease the import to cplex


def writeTestModel2():

    filename = 'Test-'  + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) + '.mod' 
    filename = PurePath('.',filename)
    with open(filename,'w') as f:

        with open('Test-header.template','r') as h:
            for line in h:
                f.write(line)


        # objective function expected value (should be extracted from filename)
        expected = 1
        # for each of the files write a line like this one
        for x in range(10,99):
            for y in range(0,9):
                file = "x_"+str(x)+"_"+str(y)+".dat"
                f.write('myTest(def, cplex,"' + file +'", logname, "SUCCESS", '+str(expected)+' );\n')

            
        with open('Test-footer.template','r') as h:
            for line in h:
                f.write(line)



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
    instance["nNurses"] = int(nNurses)
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


def generate3(nNurses, extra):

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
    instance["nNurses"] = int(nNurses)
    instance["maxConsec"] = maxConsec_base + randrange(maxConsec_variability)
    instance["maxPresence"] = maxPresence_base + randrange(maxPresence_base_variability)
    instance["maxHours"] = maxHours_base + randrange(maxHours_base_variability)
    instance["minHours"] = minHours_base + randrange(int(minHours_base_variability))

    instance["nNurses"] = int(nNurses)
    instance["maxConsec"] = maxConsec_base 
    instance["maxPresence"] = maxPresence_base 
    instance["maxHours"] = maxHours_base 
    instance["minHours"] = minHours_base 
    instance["hours"] = 24


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
    instance["nNurses-limit"]=int(nNurses)
    instance["surplus"] = round((extra/nNurses - 1)*100)
    instance["nNurses"] = int(extra)

    return instance


def metaGenerate3(n,extra, path):
    instances = generate3(n, extra)
    write(instances,"manual",path)

def metaMetaGenerate3(path, nmin=400,nmax=500, minpct=20, maxpct=30):

    for j in range(nmin,nmax,5):
        print("j="+str(j))
        lastIteration = 0
        for i in range(100+minpct,100+maxpct,1):
            extra=int(j*float((100 + maxpct) - i + (100 + minpct))/100.0)

            if extra!=lastIteration:
                print(extra)
                metaGenerate3(n=j,extra=extra, path=p)

            lastIteration=extra









def gen4Concentrated(w,start,hours,  maxConsec,maxConsecSave, minHours, maxHours, maxPresence):

    # init w
    if w == []:
        w = [ 0 for i in range(1,hours + 1) ]

    # choose a start point
    i = int(start)
    #print("-----------------gen4Concetrated:")
    #print(i)
    #print(hours)



    # put maxConsec+rest+maxConsec until maxHours or maxPresence is over
    
    print("maxConsecSave="+str(maxConsecSave))
    while ( i<= hours and  maxHours >0 and maxPresence>0):
        
        # work hours
        
        while(i<=hours and maxConsec>0):
            w[int(i-1)] = 1
            maxConsec -=1
            maxHours -=1
            maxPresence -=1
            minHours =max(0,minHours - 1)

            print(w)
            print("i="+str(i-1))
            print("maxConsec="+str(maxConsec))
            i+=1
            #print("after i+=1")
            #print(i)
 

        # rest
        if(i<=hours):
            w[int(i-1)]=0
            maxPresence -=1
            i+=1
            maxConsec=maxConsecSave
            print("adding a 0 at " + str(i-1)+ " restoring maxConsec to maxConsec="+str(maxConsec))
            print(w)
          




    print("concentrated:")
    print(w)
    print(( minHours, maxHours, maxPresence, maxConsec))
    return w, minHours, maxHours, maxPresence, maxConsec

def gen4Sparse(w,start,hours, maxConsec,maxConsecSave, minHours, maxHours, maxPresence):

    # init w
    if w == []:
        w = [ 0 for i in range(1,hours + 1) ]
    
    # choose a start point
    i = start

    # put 1hour+rest until maxPresence or maxHours
    while ( i<= hours and  maxHours >0 and maxPresence>0):
        
        # work hours
        if(i<=hours and maxConsec>0):
            w[int(i-1)] = 1
            maxConsec -=1
            maxHours -=1
            maxPresence -=1
            minHours -=1
            print("i="+str(i-1))
            print(w)


            i+=1

        # rest
        if(i<=hours):
            w[int(i-1)]=0
            maxPresence -=1
            i+=1
            maxConsec=maxConsecSave
            print("adding a 0 at " + str(i-1)+ " restoring maxConsec to maxConsec="+str(maxConsec))
            print(w)

    print("sparse:")
    print(w)
    print(( minHours, maxHours, maxPresence, maxConsec))
    return w, minHours, maxHours, maxPresence, maxConsec



def new_instance4(hours, nNurses, maxPresence, maxConsec, minHours, maxHours, numCentroides, prob, std):
    """
        creats a scheduling shape corresponding to numCentroides
            -> some randomness:
                where are the centroides placed between 1-hours?
                random but with some minimal distance between centroids
            -> uses 4 fixed shapes? then draws the selected shape more often than the others
                Prob(selectedShape) > 0.5 but randomly assign 0.5 + rand(0.5)
            -> each shape type could be added some variance also..
            -> shapes should respect maxPresence, maxConsec, minHours, maxHours and maxRest(=1)

            -> init hour could also be sligthly modified

    """
    maxConsecSave = maxConsec

    select = float(randrange(0,10,1) / 10.0)
    shapes = [0,1,2,3,4]
    w  = [0]*hours

    if numCentroides > shapes[-1]:
        numCentroides = shapes[-1]

    #if select <= prob:
    #    # choose desired shape
    #    w = get_shape(hours, nNurses, maxPresence, maxConsec, minHours, maxHours, numCentroides, prob, std)

    if select > prob:
        # remove the selected one
        shapes.pop(numCentroides)

        # choose another shape randomly
        another = randrange(len(shapes))
        
        numCentroides = shapes[another]

    
    if numCentroides == 0:
        # numcentroides is 0
        print(" centroides:  0 , flat schedule")
        hstart_top = max(2,hours - 2*minHours + 1)
        hstart = randrange(1,hstart_top)
        w, minHours, maxHours, maxPresence, maxConsec = gen4Sparse(w, hstart,hours, maxConsec,maxConsecSave,minHours, maxHours, maxPresence)

    else:
        # place centroides in [1, hours] (with some variability)

        centroides_separation = int(math.ceil(hours/(numCentroides+1)))
        centroides = [x for x in range(
                                    1 + int(randrange(0,std)) ,
                                    hours, 
                                    centroides_separation + randrange(0, int(math.ceil(std/3.0))),
                                    ) 
                        ]
        print(" centroides:")
        print(centroides)

        # for each Centroide:
        #   select hini with std
        #   put hours until maxConsec or maxPresence or maxHours or end of variability
        #   if maxConsec, put a rest then continue putting hours
        # in between centroides put sparse
        # for every assigned hour, verify maxHours, maxConsec and maxPresence

        hlast = 0
        first_hstart = hours
        for centroide in centroides:
            hstart = max(1,hlast+1, int(centroide - max(1,round(std/2,0))))
            hend = min(hours,int(centroide + max(1,round(std/2,0))))
            first_hstart = min(first_hstart,hstart)

            # add sparse work hours between centroides
            if hlast > 0 and hlast < (hstart - 1):
                print("adding sparse between: "+str(hlast)+", "+str(hstart - 1))
                print("")
                w, minHours, maxHours, maxPresence, maxConsec = gen4Sparse(w, hlast,hstart - 1, maxConsec,maxConsecSave,minHours, maxHours, maxPresence)
               

            # add work hours around the centroide
            print("adding concentrated between: "+str(hstart)+", "+str(hend))
            print("")
            w, minHours, maxHours, maxPresence, maxConsec = gen4Concentrated(w, hstart,hend, maxConsec,maxConsecSave,minHours, maxHours, maxPresence)

            hlast = hend

        #minHours verification
        if minHours > 0:
            print("minHours is not fulfilled!")
            #select where to place those hours
            if hlast+1 < hours - minHours:
                print("adding concentrated between: "+str(hlast+1)+", "+str(hours))
                w, minHours, maxHours, maxPresence, maxConsec = gen4Concentrated(w, hlast+1,hours, maxConsec,maxConsecSave,minHours, maxHours, maxPresence)
            else:
                #it is not possible to place more hours
                print("impossible to satisfy minHours")
                pass



    return w

def Generate4(hours, nNurses, pct_extra, maxPresence, maxConsec, minHours, maxHours, numCentroides):
    """
        Generate4:
            params:
                - hours
                - nNurses
                - maxPresence (1<i<hours)
                - maxConsec (1<i<hours)
                - minHours (1<i<maxHours)
                - maxHours (minHours<i<hours)
                - numCentroides: in [1,2,3,4]
        
            idea:
                given a set of params
        
                creats a set of shapes corresponding to numCentroides

                sums the shapes to create the demand vector, 
    
                number of shapes: nNurses, fixed by param value   

            pending:

                ok-updating maxConsec, (and applying it)
                ok-updating maxHours, 
                ok-not adding new values on previous assigned hours
                
                ok-updating minHours, and adding some if not satisfied 
                 
                ok-updating maxPresence

                ok-centroides not in the same place? 

                ok-centroides in the 1 or in the extremes      

    """

    # init extra params
    prob = 0.6 # the prob of generating the desired shape of schedule
    std = 4 # std in the placing of the centroides of the shape


    # init demand
    demand = [ 0 for i in range(1,hours+1) ]

    # init w matrix
    w=[]

    for i in range(0,nNurses):
        print("----------------------------------------------------instance:")
        nurse_schedule = new_instance4(hours, nNurses, maxPresence, maxConsec, minHours, maxHours, numCentroides, prob, std)
        print(nurse_schedule)
        w.append(nurse_schedule)
        print("--------------------------------------------------------------")
    
    # mix
    print("")
    print("sum of schedules:")
    for i in range(0,len(w)):
        print(w[i])
        for j in range(1,hours+1):
            demand[j-1]+=w[i][j-1]


    print("")
    print(demand)
    print("")

    instance={}
    instance["maxConsec"] = maxConsec
    instance["maxPresence"] = maxPresence
    instance["maxHours"] = maxHours
    instance["minHours"] = minHours
    instance["hours"] = hours
    instance["demand"] = demand
    instance["nNurses-limit"]=int(nNurses)

    extra = round((100.0 + float(pct_extra))/100.0*nNurses,0)
    instance["surplus"] = pct_extra
    instance["nNurses"] = int(extra)
    instance["centroides"] = numCentroides

    return instance


def metaGenerate4(path):
    """
       
        MetaGenerate 4:
            - play with the params randomly or exhaustively...
            - add a percentage to nNurses from 10% to 60%? (adjust)

        population
            hours fixed (easy like 5 or 6)
            for nNurses in range(1,10,):
                for maxPresence in range(4, hours):
                    for maxConsec in range(maxPresence,2):
                        for maxHours in range(4, maxPresence):
                            for minHours in range(1, maxHours):
                                for numCentroides in range (0,4):
                                    #generate 10 or 5 instances...

        # search01 - 3s  and some 300s time limit
        for hours in range (6,25,6):
            for pct_extra in range(20,70,40):
                for nNurses in [10,40,60,100,200,500,1000]:
                    maxPresence = int(hours*2/3)
                    maxConsec = int(maxPresence*2/3 - 2)
                    maxHours = int(maxPresence*2/3)
                    minHours = 2

        # around-60: variance enough between 1s and 300s
        for hours in range (12,25,6):
            for pct_extra in range(20,70,40):
                for nNurses in [40,100]:
                    maxPresence = int(hours*2/3)
                    maxConsec = int(maxPresence*2/3 - 2)
                    maxHours = int(maxPresence*2/3)
                    minHours = 2
                    #for maxPresence in range(3, hours,5):
                    #    for maxConsec in range(maxPresence,int(maxPresence/2),-4):
                    #        for maxHours in range(2, maxPresence,int(maxPresence/2)):
                    #            for minHours in range(1,maxHours,int(maxHours/2)):
                    for numCentroides in range (0,5):

        i-ng-60-64-40-24h-16mxP-8mxC-10mxH-2mnH-20171210_07-27-32270.dat,114.569,128
    

    search03
    --------
    hours = 24
    pct_extra = 60
    nNurses = 40

    for maxPresence in range(8,hours+1,8):
        for maxConsec in [int(maxPresence*2/3),int(maxPresence*1/3)]:
            for maxHours in  [int(maxPresence*2/3), int(maxPresence*1/3)]:
                for minHours in [1,int(maxHours*4/5)]:
                    for numCentroides in range (1,4):
                        instance = Generate4(
                            hours=hours, 
                            nNurses=nNurses, 
                            pct_extra=pct_extra, 
                            maxPresence=maxPresence, 
                            maxConsec=maxConsec, 
                            minHours=minHours, 
                            maxHours=maxHours, 
                            numCentroides=numCentroides)
                        write(instance,"ng",path)
                        instance = Generate4(
                            hours=hours, 
                            nNurses=nNurses, 
                            pct_extra=pct_extra, 
                            maxPresence=maxPresence, 
                            maxConsec=maxConsec, 
                            minHours=minHours, 
                            maxHours=maxHours, 
                            numCentroides=numCentroides)
                        write(instance,"ng",path)
            
    """

    """
    # 20171218 -----------------------------------------

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 80
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 160
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 260
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 500
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=2

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=1

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=4

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=2
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=4
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=6
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=9
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=7
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=5
    maxHours=5
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=4
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=16
    maxConsec=3
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=15
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 40
    maxPresence=10
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    """

    # 20171220 --------------------------------------------

    """ 
    hours = 24
    pct_extra = 60
    nNurses = 80
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=2

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 80
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=4

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 80
    maxPresence=12
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    hours = 24
    pct_extra = 60
    nNurses = 80
    maxPresence=14
    maxConsec=3
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 80
    maxPresence=16
    maxConsec=8
    maxHours=5
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 80
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=3
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)

    ####################3

    hours = 24
    pct_extra = 60
    nNurses = 160
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 260
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=numCentroides)
    write(instance,"ng",path)


    hours = 24
    pct_extra = 60
    nNurses = 500
    maxPresence=16
    maxConsec=5
    maxHours=10
    minHours=1
    numCentroides=3

    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=2)
    write(instance,"ng",path)
    instance = Generate4(
        hours=hours, 
        nNurses=nNurses, 
        pct_extra=pct_extra, 
        maxPresence=maxPresence, 
        maxConsec=maxConsec, 
        minHours=minHours, 
        maxHours=maxHours, 
        numCentroides=4)
    write(instance,"ng",path)


    """

    ### 20171227 --------------------------------------------------------------

    """

    instance = Generate4(
        hours=24, 
        nNurses=60, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=2)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=2)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=120, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=2)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=160, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=2)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=40, 
        pct_extra=30, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=2)
    write(instance,"ng",path)



    instance = Generate4(
        hours=24, 
        nNurses=60, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=4)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=4)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=120, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=4)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=160, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=4)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=40, 
        pct_extra=30, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=4)
    write(instance,"ng",path)
    

    instance = Generate4(
        hours=24, 
        nNurses=60, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=120, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=160, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=40, 
        pct_extra=30, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)


    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=40, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=120, 
        pct_extra=40, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=160, 
        pct_extra=40, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=240, 
        pct_extra=40, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=320, 
        pct_extra=40, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=120, 
        pct_extra=30, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)


    instance = Generate4(
        hours=24, 
        nNurses=60, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=120, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=160, 
        pct_extra=60, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)


    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=60, 
        maxPresence=15, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=50, 
        maxPresence=15, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=40, 
        maxPresence=15, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=30, 
        maxPresence=15, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=80, 
        pct_extra=20, 
        maxPresence=15, 
        maxConsec=5, 
        minHours=4, 
        maxHours=10, 
        numCentroides=1)
    write(instance,"ng",path)


    #--20171231----------------------------------------------------
    instance = Generate4(
        hours=24, 
        nNurses=420, 
        pct_extra=40, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=320, 
        pct_extra=35, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=320, 
        pct_extra=40, 
        maxPresence=16, 
        maxConsec=5, 
        minHours=2, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)
    instance = Generate4(
        hours=24, 
        nNurses=320, 
        pct_extra=40, 
        maxPresence=14, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)

    #--20180104-----------------------------------------------------
    """

    instance = Generate4(
        hours=24, 
        nNurses=320, 
        pct_extra=40, 
        maxPresence=14, 
        maxConsec=5, 
        minHours=1, 
        maxHours=10, 
        numCentroides=3)
    write(instance,"ng",path)

if __name__ == '__main__':


    p = Path(PurePath('../../../Instances/Pending7/'))
    metaGenerate4(path=p)



 
