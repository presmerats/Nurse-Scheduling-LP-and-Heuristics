import numpy as np
import sys

def decode(population, data):
    """
        GOAL is to minimize computer usage

        BASIC DECODER:
            encoding:
                rand key = order of assignment of the task i
                
            decoder:
                1)sort rand keys  => sort tasks (create an array of indices to the task list)

                2)assign each task to a computer by somekind of greedy cost:
                    not used = + 1000
                    costc*demand_taski
                    -> choose the min cost computer

            
                3)fitness = Summ costc*Yc + Z
                
                    costc
                    Yc : usage c
                    Z : remaining capacity


        CONCLUSION:
            convergence is better, BUT STILL GETS WORSE RESULTS THAN DECODER_BASIC!
            

    """


    for ind in population:

        # 1) create & sort list of tasks
        #print(ind['chr'])
        order=sorted(range(len(ind['chr'][:len(data["T"])])), key=lambda k: ind['chr'][k])
        #print(order)
        order_computers=sorted(range(len(ind['chr'][len(data["T"]):])), key=lambda k: ind['chr'][len(data["T"])+k])
        
        
        # 2) iteratively assign tasks to computers by order
        cost=0
        usage=[0]*len(data["C"])
        assignment = [-1]*len(data["T"])
        remaining = [1]*4
        for i in order:

            demand_i = data["T"][i]

            # assign to computers by order until capacity full
            j = 0
            while j < len(data["C"]):
                c = order_computers[j]
                if usage[c] + demand_i < data["C"][c]:
                    assignment[i] = c
                    usage[c] += demand_i
                    remaining[c] = (data["C"][c] - usage[c]) / data["C"][c]
                    j = len(data["C"])

                j += 1

   

        for computer in range(len(data["C"])):
         
            #feasibility
            if usage[computer] > data["C"][computer]:
                cost += float("inf")
            else:
                # cost
                cost += data["cost"][computer]*usage[computer] + remaining[computer]

        ind['solution']=assignment

        ind['fitness']=cost


    return(population)


    

