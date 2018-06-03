#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 22:11:22 2018

@author: shawn
"""
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
  

All games will be played simultaneously
grid information will be stored as a 3D trial x n x n array.

Game is won when m crosses/naughts in a row are 
placed horizontally, vertically or diagonally

'''
import time
import datetime
import numpy as np
import scipy as sp
from scipy import ndimage
import os

### Creates a grid of n dimensions
def init_grid(trials,n):
    return np.zeros((trials,n,n), dtype=np.int)

### Saves a given array as a csv
def save_data(score,movelist,trials,n,m):
    trials,n,m = str(trials), str(n), str(m)
    date = datetime.datetime.now().strftime('%d-%m:%H;%M')
    folder = os.path.join(os.getcwd(),'data')
    if not os.path.exists(folder):
        os.makedirs(folder)
    name = n+'x'+m+'x'+trials+':'+date
    np.savez_compressed(os.path.join(folder,name),score=score,moves=movelist)
    return 

### Moves are in a trials x n x n 3D array with each n x n array having 
### integers [0, n**2] detailing the turn number
def gen_moves(trials,n):
    moves = []
    for trial in range(0,trials):
        moves = np.concatenate((moves,np.random.permutation(n**2)))
    moves = np.reshape(moves,(trials,n,n))
    moves = np.array(moves,dtype = np.int)
    return moves

### Generates the structure arrays to be used by the check win function
def gen_struc(m):
    global struc_row, struc_col, struc_diag, struc_adiag
    struc_row = np.ones(m,dtype=np.int)
    struc_col = np.ones((1,m,1),dtype=np.int)
    struc_diag = np.reshape(np.diag(struc_row),(1,m,m))
    struc_adiag = np.reshape(np.array(list(zip(*reversed(np.diag(struc_row))))),(1,m,m))
    struc_row = np.reshape(struc_row,(1,1,m))
    #print(struc_row,struc_col,struc_diag,struc_adiag)
    return

### Checks the grid for any wins, then updating the score array with the turn
### a particular board has won
def check_win(grid,moves,score,n,m,move,player):
    ### Creates a new boolean grid containing only the player's token
    grid_to_check = (grid==player)
    #print(grid_to_check)
    ### Same sized grid showing the presence of any of the structures
    winner = np.asarray(ndimage.binary_erosion(grid_to_check, struc_row).astype(np.int))
    winner += np.asarray(ndimage.binary_erosion(grid_to_check, struc_col).astype(np.int))
    winner += np.asarray(ndimage.binary_erosion(grid_to_check, struc_diag).astype(np.int))
    winner += np.asarray(ndimage.binary_erosion(grid_to_check, struc_adiag).astype(np.int))
    #print(grid_to_check)
    ### Delete the winning grids and movesets, and add turn to score
    no_wins = len(np.unique(winner.nonzero()[0]))
    if no_wins > 0:
        win_loc = winner.nonzero()[0]
        score[win_loc]=move
        #grid = np.delete(grid,win_loc,axis = 0)
        #moves = np.delete(moves,win_loc,axis = 0)
        moves[win_loc] = np.zeros((1,n,n),dtype=np.int)
        grid[win_loc] = np.zeros((1,n,n),dtype=np.int)
    #print('score',score)
    return grid,score,moves

### Plays each move and checks for win
def play_game(sets,n,m):
    trials = 500
    scorelist = np.array((),dtype=np.int)
    movelist = np.array((),dtype=np.int)
    for i in range(sets):
        grid,moves = init_grid(trials,n),gen_moves(trials,n)
        movelist = np.append(movelist,moves)
        min_move = 2*m-2
        gen_struc(m)
        score = np.zeros(trials,dtype=np.int)
        for move in range(1,n**2+1):
            #print('move: ',move)
            ### Places the player's token at the position of the move number
            player = 2*(move % 2) - 1
            grid[moves==move-1] = player
            ### Checks if enough moves have passed to start checking
            if move > min_move:
                #print(grid)
                grid,score,moves = check_win(grid,moves,score,n,m,move,player)
        scorelist = np.append(scorelist, score)
        
    save_data(score,movelist,trials,n,m)

    return scorelist
    
def simulate(trials,n,m):
    sets = int(trials/500)
    start = time.time()
    ### Creates a 1D array to record the turn won
    score = play_game(sets,n,m)
    draw = np.sum(score==0)
    p1_win = np.sum(score%2==1)
    p2_win = trials - draw - p1_win
    return score

'''
    print('Time taken:',time.time()-start) 
    print('Games: ',trials)
    print('M,N: ', m,n)
    print('P1: ', p1_win, ' P2: ',p2_win,' Draw: ',draw)
    return score

#gen_moves(3,3)
simulate(1000,3,3)
'''

'''
a = np.zeros((3,5,5),dtype=np.int)
structure = np.diag(np.ones(3,dtype = np.int))
a[1:2,0:3,1:4] = 1
b = a[1]
structure = np.reshape(structure,(1,3,3))
print(a)
print(structure)

start = time.time()
print(ndimage.binary_erosion(a, structure=structure))
print(time.time()-start)

start = time.time()
for n in range(0,50):
    ndimage.binary_erosion(b, structure=np.ones((3,1)))
print(time.time()-start)
'''