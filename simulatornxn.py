#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import math
import random as rd
import time
import itertools

'''

For a n X n grid with the following setup:
    
            COLUMN
        0   1   ... n-1
 ROW
  0     0 | 1 | .. | 0        Crosses: 1 (starts first)
       ---|---|----|---
  1    -1 | -1| .. | 1        Naughts: -1
       ---|---|----|---
  :     : | : | .. | :        Blank: 0
       ---|---|----|---
 n-1    1 | 0 | .. | 0
  
  
grid information will be stored as a n x n array.

Game is won when m crosses/naughts in a row are 
placed horizontally, vertically or diagonally

Win scenarios are checked by splitting the n x n array
into constituent m x m arrays and 

'''

### Create a 2d  n x n array of 0s
def init_grid(n=3):
    return np.zeros((n,n))

### Create a random order of nxn moves
def generate_moves(n):
    return np.random.permutation(n**2)

### Plays move coordinate on grid
def play_move(grid,n,move,turn):
    x = int(move % n)
    y = int(move/n)
    player = 2 * (turn % 2) - 1
    grid[x,y] += player
    return grid

### Rotates the given grid by 90 deg clockwise
def rotate_grid(grid):
    return np.array(list(zip(*reversed(grid))))

### checks columns and main diagonal for win
def check_rows(subgrid,m):
    col_sum = np.sum(subgrid,axis = 0)
    col_sum = set(col_sum)
    if m in col_sum:
        return 0
    if -m in col_sum:
        return 1
    trace = np.trace(subgrid)
    if trace == m:
        return 0
    elif trace == -m:
        return 1
    return 2

### Splits n x n grid into (n-m+1) m x m subgrids,
### then checks win condition for each subgrid
def check_win(grid,n,m):
    for i,j in itertools.product(range(n-m+1),range(n-m+1)):
        subgrid = grid[0+i:m+i,0+j:m+j]
        outcome = check_rows(subgrid,m)
        if outcome != 2:
            return outcome
        outcome = check_rows(rotate_grid(subgrid),m)
        if outcome != 2:
            return outcome
    return 2

### Plays the game and add score for the winner
def play_game(score,n,m):
    grid, moves = init_grid(n), generate_moves(n)
    turn = 0
    for move in moves:
        turn += 1
        grid = play_move(grid,n,move,turn)

        min_move = m*2-1
        if turn > min_move:
            outcome = check_win(grid,n,m)
            if outcome != 2:
                score[outcome] += 1
                break
    return score


def simulate(trials,n,m):
    start = time.time()
    score = [0,0]
    for trial in range(0,trials):
        score = play_game(score,n,m)
    
    cross_score = score[0]
    naught_score = score[1]
    draw_score = trials - (cross_score + naught_score)
    time_taken = time.time() - start
        
    print("Games: ", trials)
    print("Cross: ",cross_score/trials)
    print("Naughts: ", naught_score/trials)
    print("Draws: ", draw_score/trials)
    print("Time taken: ", time_taken, "s")



simulate(1000,6,4)

















