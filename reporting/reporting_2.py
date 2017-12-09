import json
import math
import matplotlib.pyplot as plt
import os
import sys

filename="../cplex/model01/log-tests-model01-hfree-1512596874.242562.txt"
if len(sys.argv) >1:
    filename=sys.argv[1]



if not os.path.exists(filename):
    exit()

log = json.load(open(filename))

#print(log)
#exit()

results = {}
for elem in log:
    for k,v in elem.items():
        if "int_vars" in v and "time" in v:
            nNurses = v["Data"]
            i1 = nNurses.find("nNurses = ")
            i1 = i1 + 10
            i2 = i1 + nNurses[i1:].find(";")
            #print(i1)
            #print(i2)
            #print(nNurses[i1:])
            #if i2 == -1 or i1 == -1:
            #    continue
            nNurses = nNurses[i1:i2]
            results[int(nNurses)]= v["time"]

results_list = sorted(results.items())
x,y = zip(*results_list)
print(results_list)
print(x)
print(y)


# csv file
f = open(filename+".report2.csv","w")
f.write("instance,solve_time(s)\n")
for k,v in results.items():
    f.write(str(k)+","+str(v)+"\n")

f.close()

#plot
plt.plot(x,y, marker='+', color='r', ls='')

plt.xlabel('instance size')
plt.ylabel('Solve time')
#plt.axis([0, len(results), 0, max(y)])
plt.show()
