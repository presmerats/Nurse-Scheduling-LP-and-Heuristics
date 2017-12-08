import json
import math
import matplotlib.pyplot as plt
import sys
import os

filename="../cplex/model01/log-tests-model01-hfree-1512596874.242562.txt"
if len(sys.argv) >1:
    filename=sys.argv[1]

if not os.path.exists(filename):
    exit()

log = json.load(open(filename))


results = {}
for elem in log:
    for k,v in elem.items():
        if  "time" in v:
            results[k[:-4]]= float(v["time"])

results_list = sorted(results.items())
x,y = zip(*results_list)

print(results)
print(x)
print(y)

# csv file
# csv file
f = open(filename+".report3.csv","w")
f.write("instance,objective_fuction, solve_time(s)\n")
for elem in log:
    for k,v in elem.items():
        if "time" in v and "ObjectiveFunction" in v:
            f.write(str(k)+","+str(v["ObjectiveFunction"])+","+str(v["time"])+"\n")

f.close()

# plot 
fig, ax = plt.subplots() 
plt.plot(range(len(x)),y)
#plt.bar(range(len(y)),y, align='center')
plt.xticks(range(len(x)),x)

#plt.xticks(rotation='vertical')
plt.xticks(rotation=45, ha='right')

plt.xlabel('instance name')
plt.ylabel('Solve time(s)')

#fig.subplots_adjust(bottom=0.9)
fig.tight_layout()
#plt.axis([0, len(results), 0, max(y)])

plt.show()
