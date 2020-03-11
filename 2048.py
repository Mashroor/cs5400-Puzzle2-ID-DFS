#!/usr/bin/env python3
import sys
import time
from queue import Queue
from copy import deepcopy

winCond = False
#-------------------------gameBoard class definition-----------------------------
class gameBoard:
    #Constructor
    def __init__(self, x, y, z, spawnArr):
        self.spawns = spawnArr
        self.goal = z
        self.moves = ""
        self.numMoves = 0
        self.board = [[0 for i in range(x)] for j in range(y)]

    #PrettyPrint function
    def printBoard(self, timer):
        print("%d" % ((time.time() - timer) * 1000000))
        print(self.numMoves)
        print(self.moves)
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                content = print(self.board[i][j], end = " ")
            print("")

    #Check for finish condition, iterative. End on self.goal
    def checkFinish(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == self.goal:
                    return True
        return False

    #Using a spawn array, spawn new tiles in specific order
    def spawnNewTile(self):
        #Assign new value to spawned tile; replace the spawned tile to back of spawn list
        newTile = self.spawns[0]
        self.spawns.append(self.spawns.pop(0))
        self.currentPos = 0

        if self.board[0][0] == 0:
            self.board[0][0] = newTile
            return
        elif self.board[0][len(self.board[0])-1] == 0:
            self.board[0][len(self.board[0])-1] = newTile
            return
        elif self.board[len(self.board)-1][len(self.board[0])-1] == 0:
            self.board[len(self.board)-1][len(self.board[0])-1] = newTile
            return
        elif self.board[len(self.board)-1][0] == 0:
            self.board[len(self.board)-1][0] = newTile
        else:
            return

    #Following functions are for movement on board, tile collapsing
    def mvUp(self):
        self.moves += "U"
        self.numMoves += 1
        # Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1, 0, -1):
                    if self.board[j-1][i] == 0:
                        self.board[j-1][i] = self.board[j][i]
                        self.board[j][i] = 0
        # Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i]) - 1):
                if self.board[j+1][i] == self.board[j][i]:
                    self.board[j][i] = self.board[j][i] + self.board[j+1][i]
                    self.board[j+1][i] = 0
        # Re-condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i]) - 1, 0, -1):
                    if self.board[j-1][i] == 0:
                        self.board[j-1][i] = self.board[j][i]
                        self.board[j][i] = 0
        return self

    def mvDown(self):
        self.moves += "D"
        self.numMoves += 1
        # Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[j+1][i] == 0:
                        self.board[j+1][i] = self.board[j][i]
                        self.board[j][i] = 0
        # Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1, 0, -1):
                if self.board[j-1][i] == self.board[j][i]:
                    self.board[j][i] = self.board[j][i] + self.board[j-1][i]
                    self.board[j-1][i] = 0
        # Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[j+1][i] == 0:
                        self.board[j+1][i] = self.board[j][i]
                        self.board[j][i] = 0
        return self

    def mvLeft(self):
        self.moves += "L"
        self.numMoves += 1
        #Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1, 0, -1):
                    if self.board[i][j-1] == 0:
                        self.board[i][j-1] = self.board[i][j]
                        self.board[i][j] = 0
        #Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1):
                if self.board[i][j+1] == self.board[i][j]:
                    self.board[i][j] = self.board[i][j] + self.board[i][j+1]
                    self.board[i][j+1] = 0
        #Re-condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i]) - 1, 0, -1):
                    if self.board[i][j - 1] == 0:
                        self.board[i][j - 1] = self.board[i][j]
                        self.board[i][j] = 0
        return self

    def mvRight(self):
        self.moves += "R"
        self.numMoves += 1
        #Condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[i][j+1] == 0:
                        self.board[i][j+1] = self.board[i][j]
                        self.board[i][j] = 0
        # Add tiles
        for i in range(len(self.board)):
            for j in range(len(self.board[i])-1, 0, -1):
                if self.board[i][j] == self.board[i][j-1]:
                    self.board[i][j] = self.board[i][j-1] + self.board[i][j]
                    self.board[i][j-1] = 0
        #Re-condense board
        for h in range(len(self.board)):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])-1):
                    if self.board[i][j+1] == 0:
                        self.board[i][j+1] = self.board[i][j]
                        self.board[i][j] = 0
        return self

#----------------------- end of gameBoard class ---------------------------------
#ID-DFS Code
def IDDFS(tempSrc, foundChk):
    #set initial depth to 0
    depth = 0
    #for i < inf
    while (depth>=0 and not(foundChk)):
        dnew = deepcopy(tempSrc)
        #reset our source node. we need to do this every time we increase our depth
        srcCpy, foundChk = depthFirstSearch(dnew, foundChk, depth)
        #increment to next depth
        depth += 1
    #return soution and
    return srcCpy, foundChk
#DFS Code
def depthFirstSearch(input, winChk, depth):
    #establish a stack for DFS
    s = []
    #insert the initial state
    s.append(input)
    counter = 0
    while (len(s)!=0):
        # push onto stack
        b = s.pop()
        #evaluate children of b, 4 states created
        stU = deepcopy(b)
        stD = deepcopy(b)
        stL = deepcopy(b)
        stR = deepcopy(b)
        #generate move states, then determine if they're effective moves
        #If they are effective moves, add them to our stack
        stU = stU.mvUp()
        if stU.board != b.board and stU.numMoves< depth:
            stU.spawnNewTile()
            s.append(stU)
        stD = stD.mvDown()
        if stD.board != b.board and stD.numMoves< depth:
            stD.spawnNewTile()
            s.append(stD)
        stL = stL.mvLeft()
        if stL.board != b.board and stL.numMoves< depth:
            stL.spawnNewTile()
            s.append(stL)
        stR = stR.mvRight()
        if stR.board != b.board and stR.numMoves< depth:
            stR.spawnNewTile()
            s.append(stR)
        # check for win condition
        if stU.checkFinish():
            input = stU
            winChk = True
        if stD.checkFinish():
            input = stD
            winChk = True
        if stL.checkFinish():
            input = stL
            winChk = True
        if stR.checkFinish():
            input = stR
            winChk = True
    return input, winChk

#BFS Code
def breadthFirstSearch(input, winChk):
    # enqueue the initial state
    queue = Queue()
    queue.put(input)
    while (not(winChk) and not(queue.empty())):
        # push into queue
        a = queue.get()
        # evaluate children of a, 4 states created
        stU = deepcopy(a)
        stD = deepcopy(a)
        stL = deepcopy(a)
        stR = deepcopy(a)
        #generate move states
        stU = stU.mvUp()
        stD = stD.mvDown()
        stL = stL.mvLeft()
        stR = stR.mvRight()
        #determine if redundant move
        #push states into queue to be checked on next iteration
        if stU.board != a.board:
            stU.spawnNewTile()
            queue.put(stU)
        if stD.board != a.board:
            stD.spawnNewTile()
            queue.put(stD)
        if stL.board != a.board:
            stL.spawnNewTile()
            queue.put(stL)
        if stR.board != a.board:
            stR.spawnNewTile()
            queue.put(stR)
        #check for win condition
        if stU.checkFinish():
            input = stU
            winChk = True
        if stD.checkFinish():
            input = stD
            winChk = True
        if stL.checkFinish():
            input = stL
            winChk = True
        if stR.checkFinish():
            input = stR
            winChk = True
    return input, winChk

#--------------------------- Problem Solving ------------------------------------
#set timer
start_time = time.time()
#Read input.txt, or test cases
goal = int(input())
width, height = map(int, input().split())
spawnList = list(map(int, input().split()))
#instantiate a new gameBoard, then fill board with input
x = gameBoard(width, height, goal, spawnList)
for i in range(len(x.board)):
    x.board[i] = list(map(int, input().split()))

#check for solved game on input
if x.checkFinish():
    winCond = True

#Initiate ID-DFS method
x, winCond = IDDFS(x, winCond)

#finish state
#time converted to microsenconds
if winCond:
    x.printBoard(start_time)
