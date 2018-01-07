# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 21:07:25 2018

@author: Adrian Bazaga
"""
import pprint
import logging

printlog = False
printlog2 = False
printlog3 = False

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


def incremental_schedule_validation_fast(candidate_sol, d, h, nurse, checkers, verify_minHours = True, whattoreturn = 'summary', force_rest_check = False, set_end=-1):

    #print("incremental_sched_val_fast h=" + str(h), " n=" + str(nurse))

    candidate = candidate_sol["w"][nurse]

    maxHours_check = True
    maxConsec_check = True
    maxPresence_check = True
    rest_check = True
    minHours_check = True

    sumW = checkers[nurse]["sumW"]
    start = checkers[nurse]["start"]
    end = checkers[nurse]["end"]
    consec = checkers[nurse]["consec"]

    if printlog2 and nurse == 0:
        print("         complete_schedule_validation_fast:")
        print("         nurse " + str(nurse) + 
              " hour " + str(h) +
              " sumW " + str(sumW) +
              " start " + str(start) +
              " end " + str(end) +
              " consec " + str(consec) +
              " maxConsec " + str(d["maxConsec"]) +
              " minHours " + str(d["minHours"]))
        print(candidate)
        print("")

    # maxHours
    maxHours_check = sumW <= d["maxHours"]

    # maxConsec
    if consec > d["maxConsec"]:
        maxConsec_check = False

    # maxPresence 
    if end != -1 and start != -1:
        maxPresence_check = d["maxPresence"] >= end - start + 1

    if end != -1 and start != -1 and h > start:
        if candidate[h - 1] == 0 and candidate[h] == 0:
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


def complete_schedule_validation_fast(candidate_sol, d, nurse, h, checkers, verify_minHours = True, whattoreturn = 'summary', force_rest_check = False, set_end=-1):

    candidate = candidate_sol["w"][nurse]

    maxHours_check = True
    maxConsec_check = True
    maxPresence_check = True
    rest_check = True
    minHours_check = True

    sumW = checkers[nurse]["sumW"]
    start = checkers[nurse]["start"]
    end = checkers[nurse]["end"]
    consec = checkers[nurse]["consec"]

    if printlog2 and  nurse == 0:
        print("         complete_schedule_validation_fast:")
        print("         nurse " + str(nurse) + 
              " hour " + str(h) +
              " sumW " + str(sumW) +
              " start " + str(start) +
              " end " + str(end) +
              " consec " + str(consec) +
              " maxConsec " + str(d["maxConsec"]) )
        print(candidate)
        print("")


    # maxHours
    maxHours_check = sumW <= d["maxHours"]

    # maxConsec
    if consec > d["maxConsec"]:
        maxConsec_check = False

    # maxPresence
    if end != -1 and start != -1:
        maxPresence_check = d["maxPresence"] >= end - start + 1

    if end != -1 and start != -1 and h > start and h <= end:
        #print("validating rest_check")
        if candidate[h - 1] == 0 and candidate[h] == 0:
            rest_check = False
            #print(candidate)
        #print(str(rest_check))
    elif force_rest_check:
        if h - 1 >= 0 and candidate[h - 1] == 0 and candidate[h] == 0:
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





def complete_solution_validation(data, candidate, whattoreturn='summary'):
    d = data

    candidate_sol = candidate

    validity = True

    whattoreturn2 = whattoreturn
    if whattoreturn == 'check_function':
        whattoreturn2 = 'All'


    for nurse in range(len(candidate_sol["w"])):
        retval = complete_schedule_validation(candidate_sol, d, nurse, verify_minHours=True, whattoreturn=whattoreturn2)
        
        if whattoreturn == 'check_function':
            validity = retval[0] and retval[1] and retval[2] and retval[3] and retval[4] 

            if not validity:
                
                cause = " "
                if not retval[0]:
                    cause += "rest "
                
                if not retval[1]:
                    cause += "maxPresence "
                
                if not retval[2]:
                    cause += "maxConsec "

                if not retval[3]:
                    cause += "maxHours "

                if not retval[4]:
                    cause += "minHours "

                return validity, cause


        else:
            validity = retval
            if not validity:
                return False

    if whattoreturn == 'check_function':
        return validity, ""
    return validity


def checkIfCanWork(solution, h, n, data, sumW, hini=None):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]

    #print(z[n])
    #if z[n]==0:
    #    print("nurse " + str(n) + " check can work at " + str(h) + " cause hini =" + str(hini[n]) + " z[n]" + str(z[n]) + " can work?:"+ str(hini[n] < h and z[n]==0))
        
    if hini:
        if hini[n] < h and z[n]==0:
            #print("nurse " + str(n) + "cannot work at " + str(h) + " cause hini =" + str(hini[n]))
            return False

    aux = w[n][h]
    w[n][h] = 1

    # minHours validity
    verify_minHours = False
    if z[n] == 1 and hours - h + 1 < minHours - sumW[n]:
        verify_minHours=True

    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = complete_schedule_validation(solution, data, n, verify_minHours=verify_minHours, whattoreturn='All')

    # undo changes, just a verification
    w[n][h] = aux

    if rest_check and \
        maxPresence_check and \
        maxConsec_check and  \
        maxHours_check and \
        minHours_check:


        return True

    return False


def update_checkers(solution, data, n, h, newval, checkers):

    checker = checkers[n]

    #print("  update checkers, w(" + str(n) + "," + str(h) + ")=" + str(solution["w"][n][h]))

    if False  and solution["w"][n][h] == newval:
        #print(" update_checkers skpping!")
        return

    else:

        if solution["w"][n][h] == 0 and newval == 1:
            if printlog2 and n==0:
                print("   update_checkers - increment!")
            #increment
            solution["w"][n][h] = 1
            checker['sumW'] += 1
            #print("    updating sumw " + str(checker["sumW"]))
            if h>0 and solution["w"][n][h-1] == 0:
                #if start is -1 then start
                if checker["start"] == -1:
                    checker["start"] = h

                # new end
                checker["oldend"] = checker["end"]
                checker["end"] = h

                # consec = 1
                checker["consec"] = 1

                # rest is ok

            elif h>0 and solution["w"][n][h-1] == 1:
                if checker["start"] == -1:
                    # should never happend!
                    checker["start"] = h - 1

                # new end
                checker["oldend"] = h-1
                checker["end"] = h

                # consec = 1
                checker["consec"] += 1 

            elif h==0:
                checker["start"]=h
                checker["end"]=h
                checker["oldend"]=-1
                checker["consec"]=1

        elif solution["w"][n][h] == 0 and newval == 0:
            if rintlog2 and pn==0:
                print("   update_checkers - initialize with 0")
            
            #print("          sumw=" + str(checker["sumW"]))
            if h>0 and solution["w"][n][h-1] == 0:
                #if start is -1 then start
                if checker["start"] == h:
                    checker["start"] = -1

                if checker["end"] == h:
                    checker["oldend"] = h
                    checker["end"] = checker["oldend"]

                # consec = 1
                checker["consec"] = 0


            elif h>0 and solution["w"][n][h-1] == 1:
                if checker["start"] == -1:
                    # should never happend!
                    checker["start"] = h - 1

                # new end
                checker["oldend"] = h
                checker["end"] = h -1 

                # consec 
                checker["consec"] -= 1 

            elif h==0:
                checker["start"]=-1
                checker["end"]=-1
                checker["oldend"]=0
                checker["consec"]=0


        elif solution["w"][n][h] == 1 and newval == 0:
            # decrement
            if printlog2 and n==0:
                print("   update_checkers decrement")
            solution["w"][n][h] = 0
            checker['sumW'] -= 1
            if h>0 and solution["w"][n][h-1] == 0:
                #if start is -1 then start
                if checker["start"] == h:
                    checker["start"] = -1

                if checker["end"] == h:
                    checker["oldend"] = h
                    checker["end"] = checker["oldend"]

                # consec = 1
                checker["consec"] = 0


            elif h>0 and solution["w"][n][h-1] == 1:
                if checker["start"] == -1:
                    # should never happend!
                    checker["start"] = h - 1

                # new end
                checker["oldend"] = h
                checker["end"] = h -1 

                # consec = 1
                checker["consec"] -= 1 

            elif h==0:
                checker["start"]=-1
                checker["end"]=-1
                checker["oldend"]=0
                checker["consec"]=0

        else:
            if printlog2 and n==0:
                print("Strange case!"  + str(solution["w"][n][h]) + str(newval))

    if printlog2 and n==0:
        print(checkers[n])
        print(solution["w"][n])




def checkIfMustWork(solution, h, n, data, sumW, canWork_check, hini=None):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]
    aux = w[n][h]

    w[n][h] = 0

    # minHours validity
    verify_minHours = False
    if z[n] == 1 and hours - h + 1 < minHours - sumW[n]:
        verify_minHours = True

    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = incremental_schedule_validation(solution, data, n, verify_minHours=verify_minHours, whattoreturn='All', force_rest_check=False, set_end=h)

    # undo changes, just a verification
    w[n][h] = aux

    # print("CanRest w[" + str(n) + "][" + str(h) + "] = " + str(w[n][h]) + " ?:")
    # # print(rest_check)
    # print("rest_checkt " + str(rest_check))
    # print("minHours_checkt " + str(minHours_check))
    # print("maxHours_checkt " + str(maxHours_check))
    # print("maxConsec_checkt " + str(maxConsec_check))
    # print("maxPresence_checkt " + str(maxPresence_check))

    if ((not rest_check and minHours_check) or \
        (not rest_check and not minHours_check) or \
        (rest_check and not minHours_check)) and \
       maxPresence_check and \
       maxConsec_check and  \
       maxHours_check :

        # cannot rest!, verify if can work:
        # should always be true at the same time!
        if not canWork_check:
            print(" INCOHERENCE DETECTED cannot rest but cannot work!")

        return canWork_check

    return False



def checkIfCanWork_fast(solution, h, n, data, sumW, checkers, hini=None):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]


    #print("checkIfCanWOrk_fast h:"+str(h) + " n:" + str(n))
        
    if hini:
        if hini[n] < h and z[n]==0:
            #print("nurse " + str(n) + "cannot work at " + str(h) + " cause hini =" + str(hini[n]))
            return False

    aux = w[n][h]
    #w[n][h] = 1
    # update checkers
    update_checkers(solution, data, n, h, 1,checkers)
    #print(solution["w"][n][h])

    # minHours validity
    verify_minHours = False
    if z[n] == 1 and hours - h + 1 < minHours:
        verify_minHours=True



    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = complete_schedule_validation_fast(solution, data, n, h, checkers,  verify_minHours=verify_minHours, whattoreturn='All')

    # undo changes, just a verification
    #w[n][h] = aux
    update_checkers(solution, data, n, h, aux, checkers)
    #print(solution["w"][n][h])

    if printlog3:
        summin = 0
        for hmin in range(data["hours"]):
            summin += solution["w"][n][hmin]
        if summin != checkers[n]["sumW"]:
            print("found erroneous checkers[n][sumW]:" + str(checkers[n]["sumW"]) + " real sum:" + str(summin))
        if printlog3 and h==23 and summin > 0 and summin < data["minHours"] and minHours_check == True: # and checkers[n]["sumW"]>0: # and checkers[n]["sumW"]< data["minHours"]:
            print("h:" + str(h) + " verify_minhours: " + str(verify_minHours) + " minHours_check:" + str(minHours_check) + " minHours" + str(data["minHours"]) + " sumW:" + str(checkers[n]["sumW"]))
            print(w[n])
            print("")
        

    if rest_check and \
        maxPresence_check and \
        maxConsec_check and  \
        maxHours_check and \
        minHours_check:


        return True

    return False


def checkIfMustWork_fast(solution, h, n, data, sumW, canWork_check, checkers,hini=None):
    minHours = data["minHours"]
    hours = data["hours"]
    z = solution["z"]
    w = solution["w"]
    aux = w[n][h]


    solution["mustWork_count"] += 1
    #print("checkIfCMustWOrk_fast h:"+str(h) + " n:" + str(n))

    # should already be 0
    if w[n][h] == 1:
        print("srange case! checkIfMustWork_fast")
    w[n][h] = 0


    # minHours validity
    verify_minHours = False
    if z[n] == 1 and h >= hours - minHours + checkers[n]["sumW"]:
        verify_minHours = True
    
    if z[n] == 1 and h > 0 and w[n][h - 1] == 0 and w[n][h] == 0:
        verify_minHours = True

    # if z[n] == 1 and h > 0 and w[n][h - 1] == 0 and w[n][h] == 0:
    #     if data["minHours"] > checkers[n]["sumW"]:
    #         return True


    # verify max rest constraint if not working
    rest_check, maxPresence_check, maxConsec_check, maxHours_check, minHours_check = incremental_schedule_validation_fast(solution, data, h, n, checkers, verify_minHours=verify_minHours, whattoreturn='All', force_rest_check=False, set_end=h)



    # undo changes, just a verification
    w[n][h] = aux

    if printlog3:
        summin = 0
        for hmin in range(data["hours"]):
            summin += solution["w"][n][hmin]
        if summin != checkers[n]["sumW"]:
            print("found erroneous checkers[n][sumW]:" + str(checkers[n]["sumW"]) + " real sum:" + str(summin))
        if printlog3 and h==23 and summin > 0 and summin < data["minHours"]: # and checkers[n]["sumW"]>0: # and checkers[n]["sumW"]< data["minHours"]:
            print("h:" + str(h) + " verify_minhours: " + str(verify_minHours) + " minHours_check:" + str(minHours_check) + " minHours" + str(data["minHours"]) + " sumW:" + str(checkers[n]["sumW"]))
            print(w[n])
            print("")

    # print("CanRest w[" + str(n) + "][" + str(h) + "] = " + str(w[n][h]) + " ?:")
    # # print(rest_check)
    # print("rest_checkt " + str(rest_check))
    # print("minHours_checkt " + str(minHours_check))
    # print("maxHours_checkt " + str(maxHours_check))
    # print("maxConsec_checkt " + str(maxConsec_check))
    # print("maxPresence_checkt " + str(maxPresence_check))


    if z[n] == 1 and h > 0 and w[n][h - 1] == 0 and w[n][h] == 0 and data["minHours"] > checkers[n]["sumW"]:
        if minHours_check:
            print(" incohoerence in minHours check!")
        if not canWork_check:
            print(" incoherence in minHours check!")


    # if z[n] == 1 and h > 0 and w[n][h - 1] == 0 and w[n][h] == 0:
    #     if data["minHours"] > checkers[n]["sumW"]:         
    #         # print("minHours_check " + str(((not rest_check and minHours_check) or \
    #         #     (not rest_check and not minHours_check) or \
    #         #     (rest_check and not minHours_check)) and \
    #         #     maxPresence_check and \
    #         #     maxConsec_check and  \
    #         #     maxHours_check))
    #         print("minHours_check " + str(canWork_check))

    if ((not rest_check and minHours_check) or \
        (not rest_check and not minHours_check) or \
        (rest_check and not minHours_check)) and \
       maxPresence_check and \
       maxConsec_check and  \
       maxHours_check :

        # cannot rest!, verify if can work:
        # should always be true at the same time!
        if not canWork_check:
            print(" INCOHERENCE DETECTED cannot rest but cannot work!")

        return canWork_check

    return False