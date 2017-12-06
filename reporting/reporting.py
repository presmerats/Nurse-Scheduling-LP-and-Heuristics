import json
import math
import matplotlib.pyplot as plt
import os

filename="../cplex/model01/log-tests-model01-hfree-1512596874.242562.txt"
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

results = sorted(results.items())
x,y = zip(*results)

print(results)
print(x)
print(y)

plt.plot(x,y)
plt.xlabel('instance size')
plt.ylabel('Solve time')
#plt.axis([0, len(results), 0, max(y)])
plt.show()