import json
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
from random import randrange
import re
import traceback

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





def buildChart(data):
    """
        data = {
        'bi' : [],
        'bb' :[]
        }
    """
    


    # plot 
    fig, ax = plt.subplots() 

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    thehandles = []
    thelabels = []
    i = 0
    for k, v in data.items():

        filename = k
        i1 = filename.find('/')
        i2 = filename.find('-')
        mylabel = filename[i1:i2]


        bi = v['bi']
        bb = v['bb']

        j = i % len(colors)
        thecolor = colors[j]

        thehandle = plt.plot(range(len(bi)),bi, marker='.', color=thecolor, ls='-', label=mylabel)        
        plt.plot(range(len(bb)),bb, marker='.', color=thecolor, ls='-', label=mylabel)



        #plt.bar(range(len(y)),y, align='center')
        #plt.xticks(range(len(x)),x)

        #plt.xticks(rotation='vertical')
        #plt.xticks(rotation=45, ha='right')

        thehandles.append(thehandle)
        thelabels.append(mylabel)
        i +=1

    plt.xlabel('Steps')
    plt.ylabel('Best Integer/Bound')

    ax.legend(handles=thehandles, labels=thelabels, loc='upper left')

    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()
    #plt.axis([0, len(results), 0, max(y)])

    # plt.savefig(pp, format='pdf')
    # pp.close()

    plt.show()




def parsefile(fileobject, gapChart, filename):

    data = {
        'bi' : [],
        'bb' :[]
    }

    lines = fileobject.readlines()
    
    p = re.compile(r'\**[\s\t]+[0-9]+\+*[\s\t]+')
    p2 = re.compile(r'[0-9\,]+[\s\t]+[0-9\,]+[\s\t]+[0-9]+[\s\t]+[0-9\,]{1,6}\%')


    # search for the Nodes Table
    end = False     
    while len(lines)>0 and not end:
        line = lines.pop(0)
        if line.find("Node  Left")>-1:
            line = lines.pop(0)
            end = True

    # parse each line: get Best Integer, Best Bound, Gap
    end = False
    while len(lines)>0 and not end:
        line = lines.pop(0)
        if line.startswith("\n"):
            end = True
        else:
            # good lines
            # starts with "\**[\s\t]+[0-9]+\+*[\s\t]+" or "*     0"
            if  p.match(line):
                # extract Best Integer and Best Bound
                results = p2.findall(line)
                if len(results)>0:
                    # Best integer
                    result = results[0]
                    i1 = result.find(",")
                    i2 = i1 + 1 + result[i1+1:].find(",")
                    bi = result[:i1+4]
                    

                    # Best Bound
                    extra = result[i1+4:i2+5]
                    results2 = [ w for w in extra.split(" ") if "," in w]
                    # i3 = i1 + 4 + 
                    # bb = result[i3:i2+6]
                    if len(results2)>0:
                        bb = results2[0]
                        # print(" BestInteger " + str(bi) + " BestBound " + str(bb))
                        data['bi'].append(float(bi.replace(",",".")))
                        data['bb'].append(float(bb.replace(",",".")))


    # save to the data object

    gapChart[filename] = data


if __name__ == '__main__':

    results_folder = '../../Results/Pending6'
    gapChart = {}

    os.chdir(results_folder)
    for root, dirs, files in os.walk("."):
        for result in files:
            if result.endswith(".json"):
                continue
            filepath = os.path.join(root,result)
            with open(filepath,'r+') as f:
                try:
                    print(os.path.join(root,result))
                    parsefile(f, gapChart, result)
                    

                except Exception:
                    all_ok = False
                    print("Exception in " + result)
                    print("-"*60)
                    traceback.print_exc(file=sys.stdout)
                    print("-"*60)
        
    buildChart(gapChart)
