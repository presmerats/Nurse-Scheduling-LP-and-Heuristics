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
            results[int(v["int_vars"])]= v["time"]

results_list = sorted(results.items())
x,y = zip(*results_list)
print(results_list)
print(x)
print(y)


# csv file
f = open(filename+".report.csv","w")
f.write("instance,solve_time(s)\n")
for k,v in results.items():
    f.write(str(k)+","+str(v)+"\n")

f.close()

# plot 

plt.plot(x,y , marker='o', color='g', ls='')

plt.xlabel('instance size')
plt.ylabel('Solve time')
#plt.axis([0, len(results), 0, max(y)])
plt.show()
