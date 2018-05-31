#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 28 19:51:30 2018

@author: shawn
"""

import time
import datetime
import simNxN2 as sim2
import simulatornxn2s as sim2s
import simulatornxn as sim1
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


### Times a specific function for the given variables
def time_function(method,trials,n,m):
    timing = np.array(())
    reps = 4
    for i in range(reps):
        start = time.time()
        method(trials,n,int(m))
        timing = np.append(timing,(time.time() - start)/trials)

    timing = np.log(timing)
    err = np.std(timing)/np.sqrt(reps)
    return np.mean(timing),err

### Generates color scheme for plot
def gen_color():
    colors = [(1,0.6,0.6),(1,.4,.4),(1,.2,.2),(1,.0,.0),
              (.6,.8,.6),(.4,.8,.4),(.2,.8,.2),(.0,.8,.0)]
    return colors

def main():
    
    ### Formatting
    params = {
        'axes.labelsize': 5,
        'font.size': 6,
        'legend.fontsize': 3.5,
        'xtick.labelsize': 4,
        'ytick.labelsize': 4,
        'figure.figsize': [6, 4],
        'lines.linewidth': 0.5,
        'grid.linewidth': 0.2
    } 
    plt.rcParams.update(params)
    plt.figure(figsize=(3,3/1.6), dpi=300)    
    
    
    colors = gen_color()
    timings = np.array((),dtype=np.int)
    timings_err = np.array((),dtype=np.int)
    #trials = np.power(5,np.arange(6))
    trial_axis = np.arange(11)
    for method in [sim2.simulate,sim2s.simulate]:
        for n in (6,12):
            for m in (n/2,n):
                for trial in trial_axis:
                    trial = int(np.exp(trial))
                    timing,err = time_function(method,trial,n,m)
                    timings = np.append(timings,timing)
                    timings_err = np.append(timings_err,err)
                #print(timings)
    
    
    ### Rearranges the array to be of rows of constant n-m
    #timings = np.log(timings)
    print(timings)
    timings = np.reshape(timings,(8,len(trial_axis)))
    timings_err = np.reshape(timings_err,(8,len(trial_axis)))
    
    
    print(timings,timings_err)
    #trials = np.log(trials)
    
    methods=['loop: ','vector: ']
    m_types = ['n = 2m = 6','n = m = 6','n = 2m = 12','n = m = 12']
    
    for series in range(len(timings)):
        #offset = 0.25/len(timings)*series
        offset=0
        label_n = m_types[series%4]
        label_color = methods[int(series/4)]
        plt.plot(trial_axis,timings[series],color=colors[series])
        plt.errorbar(trial_axis,timings[series],yerr=timings_err[series],
                     capsize=0,ms=.5,elinewidth=.3,label=label_n,
                     fmt='o',color=colors[series])


    plt.xlabel('ln(trials)')
    plt.ylabel('ln(time / trial)')
    legend_n = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)
    red_line = mlines.Line2D([],[],color='red',label='Loop',linewidth=0.5)
    blue_line = mlines.Line2D([],[],color='green',label='Vector',linewidth=.5)
    legend_color = plt.legend(handles=[red_line,blue_line],loc=1)
    plt.gca().add_artist(legend_color)
    plt.gca().add_artist(legend_n)
    plt.grid()
    #plt.savefig('Timing subgrid vs image.png',bbox_inches='tight')
    plt.savefig('Timing vector vs loop2.png',bbox_inches='tight')
main()    