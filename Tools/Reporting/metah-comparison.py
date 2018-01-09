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
import matplotlib.dates as mdate

def buildChart(name, x,y, label1, x2,y2, label2):

    
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
        'o',
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


    # put all at the same beginning
    x = [ xi - x[0] for xi in x]
    x2 = [ xi - x2[0] for xi in x2]    

    xsecs =  mdate.epoch2num(x)
    plt.plot_date(xsecs,y,
        marker=markers[0],
        color=colors[0],
        ls=lss[0], 
        label=label1)


    x2secs =  mdate.epoch2num(x2)
    plt.plot_date(x2secs,y2,
        marker=markers[1],
        color=colors[1],
        ls=lss[1], 
        label=label2)
    
    plt.xlabel('Time (day hh:mm)')
    plt.ylabel('Objective function')
    
    ax.legend(loc='upper right', fontsize='medium')

    #fig.subplots_adjust(bottom=0.9)
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    #plt.axis([0, len(results), 0, max(y)])

    # plt.savefig(pp, format='pdf')
    # pp.close()
    plt.savefig('../../Results/Final/GRASPvsBRKGA/graphs/' + name  + '.png')

    plt.show()

    plt.close()






if __name__ == '__main__':

    results_folder = '../../Results/Final/GRASPvsBRKGA'

    parser = argparse.ArgumentParser()
    parser.add_argument("f1",help="file1 where to read results from")
    parser.add_argument("f2",help="file2 where to read results from")
    
    args = parser.parse_args()

    
    # json.load,
    results1 = json.load(open(args.f1,'r'))
    results2 = json.load(open(args.f2,'r'))


    # create x, y, x2, y2
    x=[]
    y=[]
    for elem in results1:
        if "end" in elem.keys():
            continue

        objf = elem["objf"]
        t = elem["time"]
        if objf == -1:
            continue
        else:
            x.append(t)
            y.append(objf)

    x2=[]
    y2=[]
    for elem in results2:
        if "end" in elem.keys():
            continue

        objf = elem["objf"]
        t = elem["time"]
        if objf == -1:
            continue
        else:
            x2.append(t)
            y2.append(objf)


    # labels
    if args.f1.find('brkga') >-1:
        label1='BRKGA'
        label2='GRASP'
    else:
        label2='BRKGA'
        label1='GRASP'


    # send to plot function


    buildChart('comparison_' + '{0:%Y%m%d_%H-%M-%S}'.format(datetime.now()), x,y, label1, x2,y2, label2)