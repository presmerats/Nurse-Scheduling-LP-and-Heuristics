import json
import math
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
from random import randrange

def sortlists(fileoutput, sortkey, newlist ):
    if not os.path.exists(fileoutput):
        f= open(fileoutput,'w+')
        f.close()
        
    f = open(fileoutput,'r+')
    current_lines = f.readlines()
    f.close()

    byint = []
    if current_lines:
        current_lines = current_lines.remove("instance,solve_time(s),intvars\n")

    if current_lines:
        for elem in current_lines:
            id, time, intvars = elem[:-1].split(",")
            byint.append({ 
                "id" : id , 
                "time": float(time), 
                "int_vars": int(intvars)  
                })

    if newlist and len(newlist)>0:
        if byint:
            newlist = sorted(
                byint.extend(newlist),
                key=lambda k: k[sortkey])

    f = open(fileoutput,"w+")
    f.write("instance,solve_time(s),intvars\n")
    for elem in newlist:
        f.write(elem["id"] + "," + str(elem["time"]) + ","  + str(elem["int_vars"]) + "\n")
    f.close()

    # plot
    x=[]
    y=[]
    for elem in newlist:
        if sortkey == "time":
            x.append(elem["id"]) 
        elif sortkey == "int_vars":
            x.append(str(elem["int_vars"])+"_"+str(randrange(1000)))
        else:
            x.append(elem["id"])
        y.append(elem["time"])

    
    


    # prepare pdf
    pp = PdfPages(fileoutput+'_plot.pdf')

    # plot 
    fig, ax = plt.subplots() 
    plt.plot(range(len(x)),y, marker='o', color='g', ls='')

    #plt.bar(range(len(y)),y, align='center')
    plt.xticks(range(len(x)),x)

    #plt.xticks(rotation='vertical')
    plt.xticks(rotation=45, ha='right')

    plt.xlabel('instance')
    plt.ylabel('Solve time(s)')

    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()
    #plt.axis([0, len(results), 0, max(y)])

    plt.savefig(pp, format='pdf')
    pp.close()

    plt.show()






files =[
    "log-q-x_all.json",
    "log-i-around-60.json",
    "log-i-search01.jso"
    ]

results = []
for filename in files:
    if not os.path.exists(filename):
        continue

    try:
        log = json.load(open(filename))

        for elem in log:
            for k,v in elem.items():
                if  "Solution" in v and v["Solution"].find("optimal")>-1:
                    results.append( 
                        { "id" : k , 
                          "time": float(v["time"]), 
                          "int_vars": int(v["int_vars"])  
                        } )

        print("processed: "+filename)
    except:
        print("error in "+filename)

results_bytime= sorted(results, key=lambda k: k['time'])
results_byint= sorted(results, key=lambda k: k['int_vars'])


sortlists('summary_byint.csv', 'int_vars', results_byint )
sortlists('summary_bytime.csv', 'time', results_bytime )
sortlists('summary_byid.csv', 'id', results_bytime )



