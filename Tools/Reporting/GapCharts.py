import json
import matplotlib.pyplot as plt
import sys
import os
from matplotlib.backends.backend_pdf import PdfPages
from random import randrange
import re
import traceback
from datetime import datetime
import argparse
import operator

def buildGapChart(data, name, namei):
    """
        data = {
        'gap' :[]
        }
    """
    
    # plot 
    fig, ax = plt.subplots() 

    #colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    colors = [
        'xkcd:orange',
        'xkcd:royal blue',
        'xkcd:forest green',
        'xkcd:green',
        'xkcd:purple',
        'xkcd:blue',
        'xkcd:pink',
        'xkcd:brown',
        'xkcd:red',
        'xkcd:light blue',
        'xkcd:teal',
        'xkcd:light green',
        'xkcd:magent',
        'xkcd:yellow',
        'xkcd:sky blue',
        'xkcd:grey',
        'xkcd:lime green',
        'xkcd:violet',
        'xkcd:dark green',
        'xkcd:olive',
        'xkcd:dark purple',
        
        'xkcd:tan',
        
        'xkcd:black',
        'xkcd:beige',
        'xkcd:peach',
        'xkcd:indigo',
        'xkcd:mustard'
    ]

    markers = [
        '+',
        ',',
        '^',
        '.',
        'v',
        's',
        'd',
        'o',
    ]

    lss = [
        ':',
        '-.',
        '--',
        '-',
    ]



    data_names = []

    for k, v in data.items():

        filename = k
        subnames = filename.split("-")
        mylabel = subnames[3]
        if namei is not None:
            mylabel = subnames[int(namei)]

        data_names.append(mylabel)

    data_names = sorted(data_names, 
                        key=lambda k: float(k))

    i = 0
    for k in data_names:

        found = False
        for key in data.keys():
            if key.find(k)>-1:
                v = data[key]
                found = True
                break        

        if not found:
            print("not found!")
            continue
        
        mylabel = k
        gap = v['gap']

        j = i % len(colors)
        thecolor = colors[j]

        j = i % len(markers)
        themarker = markers[j]

        j = i % len(lss)
        thels = lss[j]

        mylabel = mylabel+" nurses"
        plt.plot(range(len(gap)),gap, marker=themarker, color=thecolor, ls=thels, label=mylabel)

        #plt.bar(range(len(y)),y, align='center')
        #plt.xticks(range(len(x)),x)

        #plt.xticks(rotation='vertical')
        #plt.xticks(rotation=45, ha='right')

        i +=1

    
    plt.xlabel('Steps')
    plt.ylabel('Gap(%)')

    
    ax.legend(loc='upper right', fontsize='medium')




    #fig.subplots_adjust(bottom=0.9)
    fig.tight_layout()
    #plt.axis([0, len(results), 0, max(y)])

    # plt.savefig(pp, format='pdf')
    # pp.close()
    print(os.getcwd())
    plt.savefig('../graphs/' + name  + '_gap.png')

    plt.show()

    plt.close()


# def buildChart(data, name, gap):
#     """
#         data = {
#         'bi' : [],
#         'bb' :[]
#         }
#     """
    


#     # plot 
#     fig, ax = plt.subplots() 

#     #colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
#     colors = [
#         'xkcd:orange',
#         'xkcd:royal blue',
#         'xkcd:forest green',
#         'xkcd:green',
#         'xkcd:purple',
#         'xkcd:blue',
#         'xkcd:pink',
#         'xkcd:brown',
#         'xkcd:red',
#         'xkcd:light blue',
#         'xkcd:teal',
#         'xkcd:light green',
#         'xkcd:magent',
#         'xkcd:yellow',
#         'xkcd:sky blue',
#         'xkcd:grey',
#         'xkcd:lime green',
#         'xkcd:violet',
#         'xkcd:dark green',
#         'xkcd:olive',
#         'xkcd:dark purple',
        
#         'xkcd:tan',
        
#         'xkcd:black',
#         'xkcd:beige',
#         'xkcd:peach',
#         'xkcd:indigo',
#         'xkcd:mustard'
#     ]
#     i = 0
#     for k, v in data.items():

#         filename = k
#         subnames = filename.split("-")
#         mylabel = subnames[3]
        

#         bi = v['bi']
#         bb = v['bb']

#         j = i % len(colors)
#         thecolor = colors[j]

#         plt.plot(range(len(bi)),bi, marker='.', color=thecolor, ls='-', label=mylabel)        
#         plt.plot(range(len(bb)),bb, marker='.', color=thecolor, ls='-', label=mylabel )



#         #plt.bar(range(len(y)),y, align='center')
#         #plt.xticks(range(len(x)),x)

#         #plt.xticks(rotation='vertical')
#         #plt.xticks(rotation=45, ha='right')

#         i +=1

#     handles, labels = ax.get_legend_handles_labels()
#     hl = sorted(zip(handles, labels),
#                 key= lambda x: float(operator.itemgetter(1)[:-1]) )

#     handles2, labels2 = zip(*hl)
#     print(labels2)
#     ax.legend(handles2, labels2, loc='upper right', fontsize='small')

#     plt.xlabel('Steps( gap =' +  str(gap) + ')')
#     plt.ylabel('Best Integer/Bound')



#     #fig.subplots_adjust(bottom=0.9)
#     fig.tight_layout()
#     #plt.axis([0, len(results), 0, max(y)])

#     # plt.savefig(pp, format='pdf')
#     # pp.close()

#     plt.savefig('../graphs/' + name  + '.png')

#     plt.show()

#     plt.close()




def parsefile(fileobject, gapChart, filename):

    data = {
        'bi' : [],
        'bb' : [],
        'gap': []
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
                # results = p2.findall(line)
                # if len(results)>0:
                #     # Best integer
                #     result = results[0]
                #     i1 = result.find(",")
                #     i2 = i1 + 1 + result[i1+1:].find(",")
                #     bi = result[:i1+4]
                    

                #     # Best Bound
                #     extra = result[i1+4:i2+5]
                #     results2 = [ w for w in extra.split(" ") if "," in w]
                #     # i3 = i1 + 4 + 
                #     # bb = result[i3:i2+6]
                #     if len(results2)>0:
                #         bb = results2[0]

                #         # print(" BestInteger " + str(bi) + " BestBound " + str(bb))
                #         data['bi'].append(float(bi.replace(",",".")))
                #         data['bb'].append(float(bb.replace(",",".")))
                        
                # Gap
                results3 = [ w for w in line.split(" ") if '%' in w]
                if len(results3) > 0:
                    print("gap: " + results3[-1] )
                    gap = results3[-1][:-2].replace(",",".")
                    data['gap'].append(float(gap))


    # save to the data object

    gapChart[filename] = data


if __name__ == '__main__':

    results_folder = '../../Results/Final/ILPEvolution/nurses'

    parser = argparse.ArgumentParser()
    parser.add_argument("--folder",help="folder where to read results from")
    parser.add_argument("--nameindex",help="name index", type=int)

    args = parser.parse_args()


    if args.folder:
        results_folder = os.path.join(args.folder,'data')

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
        
    #buildChart(gapChart, 'Gap_' + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()), 0.2 )
    buildGapChart(gapChart, 'Gap_' + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()), args.nameindex)