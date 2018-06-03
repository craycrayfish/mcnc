#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 14 21:42:15 2018

@author: shawn
"""
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from simulatornxn2s import simulate
import time

'''
The generalised Naughts and Crosses Game:

    A n x n square grid 
    
            COLUMN
        0   1   ... n-1     0 | 1 | .. | 0        Crosses: 1 (starts first)
       ---|---|----|---
  1    -1 | -1| .. | 1        Naughts: -1
       ---|---|----|---
  :     : | : | .. | :        Blank: 0
       ---|---|----|---
 n-1    1 | 0 | .. | 0
    
     winner is the first player to get m tokens in a row

Investigating the change in edge of starting first as 
n, m is varied. Min n is 3, m =< n

This program will use the simulator to generate 100*(n x n)
randomly played games and compare the edge of the first player.

Edge = E(1) - E(2), where E is the expectation number of wins

'''


### Generates an array of n axes points between n and max_x
def generate_n(n,max_n):
    return np.arange(n,max_n + 1)


### Calculate the edge given m and n
def calculate_edge(m,n):
    sets = int(np.ceil(np.square(n)))
    trials = sets*500 
    score = simulate(trials,n,m)
    score[score%2==1] = 1
    score[(score%2==0)&(score!=0)] = -1
    edge = np.sum(score)/trials
    std = np.std(score)
    print(edge,std)
    pop_std = std/np.sqrt(trials)
    '''
    p1_win = np.sum(score[score==1])
    p2_win = np.sum(score[score==-1])
    draw = np.sum(score[score==0])
'''    
    return edge,pop_std


def analyse(max_n):
    start = time.time()
        
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
    
    
    color = [(.0,.0,1),(.1,.5,1),(.2,.8,1)]
    label = ['m = n','m = n-1', 'm = n-2']

### End formatting

    ### m_diff refers to the value of n-m
    m_diff = np.arange(3)
    for m in m_diff:
        n_axis = np.arange(3+m,max_n+1,dtype=np.int)
        edge_axis = np.array(())
        edge_err =np.array(())
        for n in n_axis:
            print(n-m,',',n)
            edge,err = calculate_edge(n-m,n)
            edge_axis = np.append(edge_axis,edge)
            edge_err = np.append(edge_err, err)
            
        plt.errorbar(n_axis,edge_axis,yerr=edge_err,fmt='o', ms=.5, 
                     color=color[m], label=label[m],capsize =0,
                     elinewidth=0.5)
        plt.plot(n_axis,edge_axis,color=color[m])
        
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=len(m_diff),
                   mode="expand", borderaxespad=0.)    
    plt.grid()
    plt.savefig('n=8.png',bbox_inches='tight')
    print('Time taken: ',time.time()-start)
    return
'''    
### Old code that checks for every n,m scenario for 3 >= m >= n

    for n in range(3,max_n +1):
### m follows the value of n
        n_axis = generate_n(n,max_n)
        edge_axis,edge_err = generate_edge(n,max_n)
        plt.errorbar(n_axis,edge_axis,yerr=edge_err,fmt='o', ms =1, color = 'C'+str(n),label = str(n),capsize =0,elinewidth=0.5)
    
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=max_n, mode="expand", borderaxespad=0.) 
    plt.grid()
    plt.savefig('n=8.png',bbox_inches='tight')
    
    print('Time taken: ',time.time()-start)
    return
'''



print(analyse(10))






