# -*- coding: utf-8 -*-
"""
@author: Adrian Rodrigez Bazaga, Pau Rodriguez Esmerats
"""

class Nurse:

    def __init__(self, schedule, other=None):

        if other is None:
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
            self.sumW = other.sumW
            self.consec = other.consec
            self.start = other.start
            self.end = -1
            self.rest = -1
            self.rest_1 = other.rest
            self.rest_2 = -1
            if len(schedule) > 2:
                self.rest_2 = other.rest_1

            self.gc = float("inf")       

            # update information
            if schedule[-1] == 1:
                self.sumW = other.sumW + 1
                self.consec = other.consec + 1
                if other.start == -1:
                    self.start = len(schedule)
                self.end = len(schedule)
                self.rest = 0
            else:
                self.sumW = other.sumW 
                self.consec = 0
                self.end = other.end
                self.rest = 1  


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

