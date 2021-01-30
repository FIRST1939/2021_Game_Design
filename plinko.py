# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 09:18:18 2021

@author: Sriram
"""


from numpy import array
from random import getrandbits
from collections import Counter
from tqdm import tqdm


#sample inits
#X=peg, O=empty, G1-N = the goal
board = array([
         ['|','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','|'],
         ['|','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','|'],
         ['|','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','|'],
         ['|','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','|'],
         ['|','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','|'],
         ['|','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','|'],
         ['|','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','|'],
         ['|','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','|'],
         ['|','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','X','O','|'],
         ['|','G1','O','G2','O','G3','O','G4','O','G5','O','G6','O','G7','O','G8','O','G9','|']
        ])

#Mapping from goal to points.
expectedValueMap = {'G1':6,'G2':5,'G3':4,'G4':3,'G5':3,'G6':3,'G7':4,'G8':5,'G9':6}
#Scroll all the way down to get to the function that
#you can fiddle with for a board and expectedValueMapping


def plinkoPlay(board, startPos):
   #coords stored as (x,y). y=0 means top, y increases as go down plinko
   coords = [startPos, 0]
   space = board[coords[1], coords[0]]

   while space[0] != 'G':
      space = board[coords[1], coords[0]]
      if space == 'X':
         #1 = right, 0 = left
         if getrandbits(1):
            #check if wall
            if board[coords[1], coords[0] + 1] == '|':
               coords[0] -= 1
            else:
               coords[0] += 1
         else:
            #check if wall
            if board[coords[1], coords[0] - 1] == '|':
               coords[0] += 1
            else:
               coords[0] -= 1

      coords[1] += 1

   return space


def plinkoStatTrials(board, startPos, iters):
   statTrials = []
   for i in range(iters):
      statTrials.append(plinkoPlay(board, startPos))

   statTrials = Counter(statTrials)

   for i in statTrials.keys():
      statTrials[i] /= iters

   return statTrials


def expectedValue(statTrials, expectedValueMap):
   expectedValue = 0
   for goal in statTrials.keys():
      expectedValue += statTrials[goal] * expectedValueMap[goal]

   return expectedValue


def plinkoStatStarts(board, iters, expectedValueMap=None):
   startPosList = range(1, len(board[0]) - 1)

   statStarts = {}

   if expectedValueMap:
      for startPos in tqdm(startPosList):
         statStarts[startPos] = expectedValue(plinkoStatTrials(board, startPos, iters), expectedValueMap)

   else:
      for startPos in tqdm(startPosList):
         statStarts[startPos] = plinkoStatTrials(board, startPos, iters)

   return statStarts


#plinkoStatStarts uses arguments (board, iters, expectedValueMap=None) (meaning that the last argument is optional)
#If you want the probabilities of each goal with each startPos, don't put an expectedValueMap
#iters is how many times to play plinko for each starting position
#this saves it to out because printing it looks ugly. You can print it in the terminal or add a print
#after the line if you wish. Spyder has a variable explorer, which is just what I use.
out = plinkoStatStarts(board, 100000, expectedValueMap)