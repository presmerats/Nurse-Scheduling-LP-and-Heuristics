# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 21:07:25 2018

@author: Adrian Bazaga
"""
import pprint
import logging

printlog = False

def isValid_ng(data, candidate):
    d = data

    validity = True
    maxHours_check = True
    maxConsec_check = True
    maxPresence_check = True
    rest_check = True
    minHours_check = True
    
    maxHours_check = candidate.sumW <= d["maxHours"]
    maxConsec_check = candidate.consec <= d["maxConsec"]

    if candidate.end == -1 or candidate.start == -1:
        maxPresence_check = True  # should never happend!
    else:
        maxPresence_check = d["maxPresence"] >= candidate.end - candidate.start + 1




                  
    rest_check = ((candidate.rest == 0 and candidate.rest_1 == 0) or
                  (candidate.rest == 1 and candidate.rest_1 == 0) or 
                  (candidate.rest == 1 and candidate.rest_1 == 1 and
                    candidate.rest_2 == 0  ) or
                  (candidate.rest == 0 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == -1) or
                  (candidate.rest == 0 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 1 and candidate.start == len(candidate.schedule) ) or
                  (candidate.rest == 1 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 1 and candidate.start == -1 ) or
                  (candidate.rest == 1 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 1 and candidate.end < len(candidate.schedule) - 2 ) or
                  (candidate.rest == 1 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == -1 ) or
                  (candidate.rest == 0 and candidate.rest_1 == 1 and 
                    candidate.rest_2 == 0 ) 
                  )
                   



    minHours_check = True
    if candidate.sumW < d["minHours"]  and d["hours"] - d["minHours"] + 1 <= len(candidate.schedule):
        minHours_check = candidate.sumW >= d["minHours"] - (d["hours"] - len(candidate.schedule)) 


    validity = minHours_check and \
        maxHours_check and \
        maxConsec_check and \
        maxPresence_check and \
        rest_check

    return validity

def isValid(data, candidate):
    d = data

    validity = True

    maxHours_check = True
    sumW = 0
    maxConsec_check = True
    consec = 0
    maxPresence_check = True
    start = -1
    end = -1
    rest_check = True
    rest = 0
    minHours_check = True
    for w in range(len(candidate)):

        # maxHours
        sumW += candidate[w]
        maxHours_check = sumW <= d["maxHours"]

        # maxConsec
        #   -> just need to be checked on the last consec group of hours..
        
        maxConsec_check = False
        if candidate[-1] == 0 :
            maxConsec_check = True
        else:
            consec = 0
            for w in range(len(candidate)):

                
                if candidate[len(candidate) - w - 1] == 0:
                    maxConsec_check = True
                    break
                else:
                    consec += 1
                    if consec > d["maxConsec"]:
                        maxConsec_check = False
                        break
                
            
            maxConsec_check = consec <= d["maxConsec"]

            #print("maxconsec " + str(d["maxConsec"]) + " consec:" + str(consec))

        # maxPresence
        start = -1
        for w in range(len(candidate)):
            if candidate[w] == 1:
                start = w + 1
                break
        end = -1
        for w in range(len(candidate)):
            if candidate[len(candidate) - w - 1] == 1:
                end = len(candidate) - w
                break

        if end == -1 or start == -1:
            maxPresence_check = True  # should never happend!
        else:
            maxPresence_check = d["maxPresence"] >= end - start + 1

        #print("maxPresence "+str(d["maxPresence"])+" start:"+str(start)+" end:"+str(end))

        # rest
        if candidate[-1] == 1:
            rest_check = True
        else:
            if candidate[-2] == 1:
                rest_check = True
            elif candidate[-2] == 0 and start < len(candidate) - 2 and end > len(candidate) - 2:
                rest_check = False
            else:
                rest_check = True

        # minHours (only if hours - minHours + 1 <= len(candidate))
        minHours_check = True
        if sumW < d["minHours"]  and d["hours"] - d["minHours"] + 1 <= len(candidate):
            #print("sumW: " + str(sumW) + " >= " + str(d["minHours"]) + "-" + str(d["hours"]) + "+" + str(len(candidate)) + " minHours_check: " + str(minHours_check))

            minHours_check = sumW >= d["minHours"] - (d["hours"] - len(candidate))

        validity = minHours_check and \
            maxHours_check and \
            maxConsec_check and \
            maxPresence_check and \
            rest_check
        
    return validity

def isFeasible(solution, data):
    """
        feasibility:
            - all demand is fulfilled
    """
    
    d = data["demand"]
    w = solution["w"]
    served = True
    for h in range(len(d)):

        sum_nurses = 0
        for n in range(len(w)):
            sum_nurses += w[n][h]

        if d[h] > sum_nurses:
            served = False
            break

    return served

def incremental_schedule_validation(candidate_sol, d, nurse, verify_minHours = True, whattoreturn = 'summary', force_rest_check = False, set_end=-1):

    candidate = candidate_sol["w"][nurse]

    maxHours_check = True
    sumW = 0
    maxConsec_check = True
    consec = 0
    maxPresence_check = True
    start = -1
    end = -1
    rest_check = True
    minHours_check = True

    stop = len(candidate)
    if set_end > -1:
        stop = set_end + 1

    for w in range(stop):

        # maxHours
        sumW += candidate[w]
        maxHours_check = sumW <= d["maxHours"]

        # maxConsec
        if candidate[stop - w - 1] == 0:
            consec = 0
        else:
            consec += 1
            if consec > d["maxConsec"]:
                maxConsec_check = False

        # maxPresence
        if start == -1:
            if candidate[w] == 1:
                start = w + 1
                
        if candidate[w] == 1:
            end = w + 1

        if end != -1 and start != -1:
            maxPresence_check = d["maxPresence"] >= end - start + 1

        if end != -1 and start != -1 and w > start:
            if candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False
        elif force_rest_check:
            if w - 1 >= 0 and candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False

        # minHours (only if hours - minHours + 1 <= len(candidate))
        if sumW > 0 and verify_minHours:
            minHours_check = sumW >= d["minHours"]

    validity = minHours_check and \
        maxHours_check and \
        maxConsec_check and \
        maxPresence_check and \
        rest_check

    if not validity:

        if printlog:
            print("validity: ")

            print(candidate)
            print(data)
            print("minHours: " + str(minHours_check))
            print("maxHours: " + str(maxHours_check))
            print("consec:   " + str(maxConsec_check))
            print("Presence: " + str(maxPresence_check))
            print("rest:     " + str(rest_check))
            print("=")
            print(validity)

    if whattoreturn == 'All':
        return (rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check )
    elif whattoreturn == 'rest':
        return rest_check
    elif whattoreturn == 'presence':
        return maxPresence_check
    elif whattoreturn == 'consec':
        return maxConsec_check
    elif whattoreturn == 'maxhours':
        return maxHours_check
    elif whattoreturn == 'minhours':
        return minHours_check

    return validity

def complete_schedule_validation(candidate_sol, d, nurse, verify_minHours = True, whattoreturn = 'summary', force_rest_check = False, set_end=-1):

    candidate = candidate_sol["w"][nurse]

    maxHours_check = True
    sumW = 0
    maxConsec_check = True
    consec = 0
    maxPresence_check = True
    start = -1
    end = -1
    rest_check = True
    minHours_check = True

    stop = len(candidate)
    if set_end > -1:
        stop = set_end + 1

    # look for end
    end = -1
    for h in range(len(candidate)):
        if candidate[h]==1:
            end = h

    for w in range(stop):

        # maxHours
        sumW += candidate[w]
        maxHours_check = sumW <= d["maxHours"]

        # maxConsec
        if candidate[len(candidate) - w - 1] == 0:
            consec = 0
        else:
            consec += 1
            if consec > d["maxConsec"]:
                maxConsec_check = False

        # maxPresence
        if start == -1:
            if candidate[w] == 1:
                start = w + 1
        if end == -1:
            if candidate[len(candidate) - w - 1] == 1:
                end = len(candidate) - w
        if end != -1 and start != -1:
            maxPresence_check = d["maxPresence"] >= end - start + 1

        if end != -1 and start != -1 and w > start and w <= end:
            #print("validating rest_check")
            if candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False
                #print(candidate)
            #print(str(rest_check))
        elif force_rest_check:
            if w - 1 >= 0 and candidate[w - 1] == 0 and candidate[w] == 0:
                rest_check = False

        # minHours (only if hours - minHours + 1 <= len(candidate))
        if sumW > 0 and verify_minHours:
            minHours_check = sumW >= d["minHours"]

    validity = minHours_check and \
        maxHours_check and \
        maxConsec_check and \
        maxPresence_check and \
        rest_check

    if not validity:

        if printlog:
            print("validity: ")

            print(candidate)
            print(data)
            print("minHours: " + str(minHours_check))
            print("maxHours: " + str(maxHours_check))
            print("consec:   " + str(maxConsec_check))
            print("Presence: " + str(maxPresence_check))
            print("rest:     " + str(rest_check))
            print("=")
            print(validity)

    if whattoreturn == 'All':
        return (rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check )
    elif whattoreturn == 'rest':
        return rest_check
    elif whattoreturn == 'presence':
        return maxPresence_check
    elif whattoreturn == 'consec':
        return maxConsec_check
    elif whattoreturn == 'maxhours':
        return maxHours_check
    elif whattoreturn == 'minhours':
        return minHours_check

    return validity


def complete_solution_validation(data, candidate):
    d = data

    candidate_sol = candidate

    validity = True

    for nurse in range(len(candidate_sol["w"])):
        validity = validCandidate(candidate_sol, d, nurse)
        if not validity:
            return False

    return validity