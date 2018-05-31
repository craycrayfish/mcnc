#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 27 17:45:54 2018

@author: shawn
"""

import time
import datetime
import simNxN2 as sim2
import simulatornxn2s as sim2s
import simulatornxn as sim1
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

### Times a specific function for the given variables
def time_function(method,trials,n,m):
    timing = np.array(())
    reps = 4
    for i in range(reps):
        #for trial in trials:
        start = time.time()
        method(trials,n,m)
        timing = np.append(timing,(time.time() - start)/trials)

    timing = np.log(timing)
    err = np.std(timing)/np.sqrt(reps)
    return np.mean(timing),err

### Generates color scheme for plot
def gen_color():
    colors = [(1,0.6,0.6),(1,.4,.4),(1,.2,.2),(1,.0,.0),
              (.6,.6,1),(.4,.4,1),(.2,.2,1),(.0,.0,1)]
    return colors

def main(n):
    
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
    trials = 50
    n_axis = np.arange(6,n)
    for method in [sim2.simulate,sim1.simulate]:
        for n in n_axis:
            for m in range(n-3,n+1):
                timing,err = time_function(method,trials,n,m)
                timings = np.append(timings,timing)
                timings_err = np.append(timings_err,err)
                #print(timings)
    
    
    ### Rearranges the array to be of rows of constant n-m
    #timings = np.log(timings)
    timings = np.reshape(timings,(2,len(n_axis),4))
    timings_err = np.reshape(timings_err,(2,len(n_axis),4))
    
    time_axis = np.array(())
    time_err = np.array(())
    for axis in range(len(timings)):
        time_axis=np.append(time_axis,np.transpose(timings[axis]))
        time_err=np.append(time_err,np.transpose(timings_err[axis]))
        
    timings = np.reshape(time_axis,(8,len(n_axis)))
    timings_err = np.reshape(time_err,(8,len(n_axis)))
    
    print(timings,timings_err)
    #trials = np.log(trials)
    
    methods=['subgrid: ','image: ']
    m_types = ['m = n-3','m = n-2','m = n-1','m = n']
    
    for series in range(len(timings)):
        #offset = 0.25/len(timings)*series
        offset=0
        label_m = m_types[series%4]
        label_color = methods[int(series/4)]
        plt.plot(n_axis+offset,timings[series],color=colors[series])
        plt.errorbar(n_axis+offset,timings[series],yerr=timings_err[series],
                     capsize=0,ms=.5,elinewidth=.3,label=label_m,
                     fmt='o',color=colors[series])

    plt.xlabel('N')
    plt.ylabel('ln(time/trial (out of 50))')
    legend_n = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)
    red_line = mlines.Line2D([],[],color='red',label='Loop',linewidth=0.5)
    blue_line = mlines.Line2D([],[],color='blue',label='Vector',linewidth=.5)
    legend_color = plt.legend(handles=[red_line,blue_line],loc=4)
    plt.gca().add_artist(legend_color)
    plt.gca().add_artist(legend_n)
    plt.grid()
    plt.savefig('Timing subgrid vs image2.png',bbox_inches='tight')
    #plt.savefig('Timing vector vs no.png',bbox_inches='tight')
    
    
main(14)    











