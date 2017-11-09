import numpy as np
from random import randrange
import pprint
from datetime import datetime
#import matplotlib.pyplot as plt


def write(instance):
    
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(instance)

    filename = 'instance-' + str(instance["nNurses"]) +'-' + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()) + '.dat' 
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



def generate(i):


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

if __name__ == '__main__':

    instances = generate(100)
    write(instances)