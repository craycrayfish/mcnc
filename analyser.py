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
from simNxN2 import simulate
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
    trials = 400*np.square(n)
    score = simulate(trials,n,m)   
    score[score%2==1] = 1
    score[(score%2==0)&(score!=0)] = -1
    edge = np.sum(score)/trials
    std = np.std(score)
    pop_std = std/np.sqrt(trials)
    '''
    p1_win = np.sum(score[score==1])
    p2_win = np.sum(score[score==-1])
    draw = np.sum(score[score==0])
'''    
    return edge,pop_std


### Generates an edge for each of the n,m cases,
### where m ranges from 3 to n
def generate_edge(n, max_n):
    edge_axis = []
    edge_err = []
### m takes the value of n
    for grid_size in range(n,max_n+1):
        edge,err = calculate_edge(n,grid_size)
        edge_axis = np.append(edge_axis,edge)
        edge_err = np.append(edge_err,err)
    return edge_axis,edge_err




def analyse(max_n):
    start = time.time()
        
### Formatting 
    params = {
        'axes.labelsize': 6,
        'font.size': 6,
        'legend.fontsize': 6,
        'xtick.labelsize': 6,
        'ytick.labelsize': 6,
        'figure.figsize': [6, 4]
    } 
    plt.rcParams.update(params)
    plt.figure(figsize=(3,3/1.6), dpi=400)    
    
    color = ['red','orange','yellow','green','blue','violet']


### End formatting
    
    for n in range(3,max_n +1):
### m follows the value of n
        n_axis = generate_n(n,max_n)
        edge_axis,edge_err = generate_edge(n,max_n)
        plt.errorbar(n_axis,edge_axis,yerr=edge_err,fmt='o', ms =1, color = 'C'+str(n),label = str(n),capsize =0,elinewidth=0.5)
    
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=max_n, mode="expand", borderaxespad=0.) 
    plt.grid()
    plt.savefig('8x8case-4.png',bbox_inches='tight')
    
    print('Time taken: ',time.time()-start)
    return




print(analyse(8))






