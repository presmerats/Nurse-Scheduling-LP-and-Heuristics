import numpy as np
import sys

def decode(population, data):
    """
        Idea 1)
            CHR = first work hour of the nurse

        Idea 2)
            CHR[i] = hi -> nursei start working at hi OR BEFORE

        Idea 3)
            CHR[i] = hi -> nursei start working at hi OR AFTER
            
    """


    for ind in population:

        # 1) transform from 0.xx to hini

        hours = data["hours"]
        # improvement?, use the first hour with demand, instead of 1...

        hini = [int(hours * ci) for ci in ind['chr']]

        print(hini)


        # 2) assign work hours to nurses
        assignment = {
            "cost": 0,
            "w": [],
            "z": [0] * data["nNurses"],
            "last_added": 0,
            "pending": [0] * data["hours"],
            "totalw": 0,
            "exceeding": [0] * data["hours"]
        }

        ind['solution']=assignment

        ind['fitness']=assignment["cost"]

    return(population)