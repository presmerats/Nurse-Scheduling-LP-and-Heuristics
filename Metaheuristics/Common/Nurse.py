# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 18:29:40 2017

@author: Adrian Rodrigez Bazaga, Pau Rodriguez Esmerats
"""

class Nurse:

    def __init__(self, schedule, element=None):

        if element is None:
            self.schedule = schedule
            self.sumW = 0
            self.consec = 0
            self.start = -1
            self.end = -1
            self.rest = -1
            self.rest_1 = -1
            self.rest_2 = -1
            self.gc = float("inf")
        else:

            self.schedule = schedule
            self.sumW = element.sumW
            self.consec = element.consec
            self.start = element.start
            self.end = -1
            self.rest = -1
            self.rest_1 = element.rest
            self.rest_2 = -1
            if len(schedule) > 2:
                self.rest_2 = element.rest_1

            self.gc = float("inf")       

            # update information
            if schedule[-1] == 1:
                self.sumW = element.sumW + 1
                self.consec = element.consec + 1
                if element.start == -1:
                    self.start = len(schedule)
                self.end = len(schedule)
                self.rest = 0
            else:
                self.sumW = element.sumW 
                self.consec = 0
                self.end = element.end
                self.rest = 1  

            #element.myprint()
        
        #self.myprint()


    def myprint_long(self):
        pp.pprint(self.schedule)
        pp.pprint(self.gc)
        pp.pprint(self.start)
        pp.pprint(self.end)
        pp.pprint(self.sumW)
        pp.pprint(self.rest)
        pp.pprint(self.rest_1)
        pp.pprint(self.consec)
        print("")

    def myprint(self):
        pp.pprint(self.schedule)
        pp.pprint(self.gc)
        print("")

    def myprint_short(self):
        pp.pprint(self.schedule)

