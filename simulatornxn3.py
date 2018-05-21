#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:42:01 2018

@author: shawn
"""

import numpy as np
import math
import random as rd
import time
import itertools

'''
For a n X n grid with the following setup:

            COLUMN
 ROW    0   1   ... n-2 n-1

  0     0 | 0 | .. | 0 | 0 |    Crosses: 1 (starts first)
       ---|---|----|---|---|
  1     0 | -1| .. | 1 | 0 |    Naughts: -1
       ---|---|----|---|---|
  :     : | : | .. | : | : |    Blank: 0
       ---|---|----|---|---|
 n-2    0 | 1 | .. | -1| 0 |
       ---|---|----|---|---|
 n-1    0 | 0 | .. | 0 | 0 |

grid information will be stored as a n x n array.
leave the boundary with 0s to make it look beautiful
Game is won when m crosses/naughts in a row are 
placed horizontally, vertically or diagonally


'''

### Creates a grid of n dimensions
def init_grid(n):
    return np.zeros((n,n), dtype=np.int)


### Generates randomised iterable coordinates with every point
def gen_moves(n):
    moves = np.random.permutation(n**2)
    x = np.array(moves % n,dtype=int)
    y = np.array(moves/n,dtype=int)

    return zip(x,y)



def check_win(grid,n,m,player,move):
    





### Given n and m, plays a random game and returns the turn in which
### game is won. 0 is for draws
def play_game(n,m):
    grid,moves = init_grid(n),gen_moves(n)
    turn = 0
    min_move = 2*m-2
    for move in moves:
        turn += 1
        player = 2*(turn % 2) - 1
        grid[move[0],move[1]] = player

        if turn > min_move:
            if check_win(grid,n, m,player,move):
                return turn
    print(grid)
    return 0


def simulate(trials,n,m):
    start = time.time()
    score = np.array((),dtype=np.int)
    for trial in range(0,trials):
        ### Adds the turn in which game is won
        score = np.append(score,[play_game(n,m)])
    
    turn,occurences = np.unique(score,return_counts=True)
    result = np.array(list(zip(turn,occurences)))
    print('Time taken v2:',time.time()-start) 
    try: 
        draw = occurences[turn==0][0]
    except:
        draw = 0
    p1_win = np.sum(occurences[turn%2==1])
    p2_win = np.sum(occurences[turn%2==0])- draw
    

    return np.array((p1_win,p2_win))
    




def timeit(function):
    start = time.time()
    for n in range(0,100):
        function
    return time.time()-start

print(timeit(gen_moves(9)))








