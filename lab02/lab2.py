# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 10:48:29 2020

@author: Marius
"""

from time import time
import copy
import math

class Configuration:
    def __init__(self, columns):
        self.__size = len(columns)
        self.__values = columns[:]
        
    def getSize(self):
        return self.__size
    
    def getValues(self):
        return self.__values[:]
    
    def __eq__(self, other):
        if not isinstance(other, Configuration):
            return False
        if self.__size != other.getSize():
            return False
        for i in range(self.__size):
            if self.__values[i] != other.getValues()[i]:
                return False
        return True
    
    def findFirstEmpty(self):
        if -1 in self.__values:
            return self.__values.index(-1)
        else:
            return -1
        
    def checkSolution(self):
        l = self.getSize()
        if -1 in self.getValues():
            return False
        for i in range(l):
            if self.getValues().count(i) > 1:
                return False
        count = 0
        revList = self.getValues()[::-1]
        for i in range(l - 1):
            if(revList[i] != -1 and revList[i+1] != -1):
                if abs(revList[i] - revList[i+1]) < 2:
                    count += 1
        if count == 0:
            return True
        else:
            return False
    
    def __str__(self):
        l = self.getSize()
        board = []
        for i in range(l):
            row = []
            for j in range(l):
                row.append(0)
            board.append(row)
        for i in range(l):
            if self.getValues()[i] != -1:
                board[i][self.getValues()[i]] = 1
            
        square = int(math.sqrt(l))
        res = "\n"
        for i in range(l):
            partialRes = "  "
            for j in range(l):
                partialRes += str(board[i][j])
                if j % square == square - 1:
                    partialRes += " "
                else:
                    partialRes += " "
            partialRes += "\n"
            length = len(partialRes)
            beginning = ""
            if i % square == square - 1:
                for x in range(length - 2):
                    pass
                    #partialRes += " "
                    #beginning += " "
                #partialRes += "\n"
            res += partialRes
        
        return str(beginning) + str(res)
                
        #return str(self.__values)
    
    def nextConfig(self):
        myList = []
        l = self.getSize()
        values = copy.deepcopy(self.getValues())
        firstEmpty = self.findFirstEmpty()
        if firstEmpty != -1:
            for j in range(l):
                values[firstEmpty] = j
                myList.append(Configuration(values))
        return myList
    
class State:
    def __init__(self):
        self.__values = []
        
    def setValues(self, values):
        self.__values = values[:]
        
    def getValues(self):
        return self.__values[:]
    
    def __str__(self):
        s = ''
        for x in self.__values:
            s += str(x) + "\n"
        return s
    
    def __add__(self, something):
        aux = State()
        if isinstance(something, State):
            aux.setValues(self.__values + something.getValues())
        elif isinstance(something, Configuration):
            aux.setValues(self.__values + [something])
        else:
            aux.setValues(self.__values)
        return aux
    
class Problem:
    def __init__(self, initial):
        self.__initialConfig = initial
        self.__initialState = State()
        self.__initialState.setValues([self.__initialConfig])
        
    def expand(self, currentState):
        '''
        myList = []
        currentConfig = currentState.getValues()[-1]
        firstEmpty = currentConfig.findFirstEmpty()
        if firstEmpty != -1:
            for j in range(currentConfig.getSize()):
                aux = currentConfig.getValues()[:]
                aux[firstEmpty] = j
                myList.append(aux)
        return myList
        '''
        myList = []
        currentConfig = currentState.getValues()[-1]
        #for j in range(currentConfig.getSize()):
        for x in currentConfig.nextConfig():
            myList.append(currentState + x)
        return myList
    
    
    def getRoot(self):
        return self.__initialState
    
    def heuristics(self, state):
        if -1 in state.getValues()[-1].getValues():
            return 0
        currentConfig = state.getValues()[-1]
        revList = currentConfig.getValues()[::-1]
        count = currentConfig.getSize()
        for i in range(currentConfig.getSize() - 1):
            if(revList[i] != -1 and revList[i+1] != -1):
                if abs(revList[i] - revList[i+1]) < 2:
                    count -= 1
        return count
    
class Controller:
    def __init__(self, problem):
        self.__problem = problem
        
    def DFS(self, root):
        q = [root]
        visited = set()
        visited.add(root)
        
        while len(q) > 0:
            currentState = q.pop()
            if currentState.getValues()[-1].checkSolution():
                return currentState
            newStates = self.__problem.expand(currentState)
            for state in newStates:
                if state not in visited:
                    visited.add(state)
                    q.append(state)

        
    def Greedy(self, root):
        
        found = False
        visited = []
        toVisit = [root]
        while len(toVisit) > 0 and not found:
            node = toVisit.pop(0)
            visited = visited + [node]
            if node.getValues()[-1].checkSolution():
                return node
            aux = []
            for x in self.__problem.expand(node) :
                if x not in visited:
                    aux.append(x)
            aux = [ [x, self.__problem.heuristics(x)] for x in aux]
            aux.sort(key=lambda x:x[1])
            aux = [x[0] for x in aux]
            toVisit = aux[:] + toVisit
        '''
        currentState = root
        currentHeuristic = self.__problem.heuristics(currentState)
        while True:
            if currentState.getValues()[-1].checkSolution():
                return currentState
            newStates = self.__problem.expand(currentState)
            bestHeuristic = 0
            for state in newStates:
                if self.__problem.heuristics(state) > bestHeuristic:
                    bestHeuristic = self.__problem.heuristics(state)
                    auxState = state
            if bestHeuristic > currentHeuristic:
                currentState = auxState
            else:
                #Can find no better solution
                return currentState
        '''
        
class UI:
    def __init__(self):
        self.__iniC = Configuration([-1,-1,-1,-1])
        self.__p = Problem(self.__iniC)
        self.__contr = Controller(self.__p)
        
    def printMainMenu(self):
        s = ''
        s += "[0,0,0,0] if you don't have any imagination \n"
        s += "0 - exit \n"
        s += "1 - read number of queens \n"
        s += "2 - find solution with DFS \n"
        s += "3 - find solution with Greedy \n"
        print(s)
        
    def readConfigSubmenu(self):
        n = 4
        try:
            print("Input number of queens (implicit n=4)")
            n = int(input("n = "))
        except:
            print("Invalid number, the implicit value is still 4")
            n = 4
        self.__iniC = Configuration( [-1] * n)
        self.__p = Problem(self.__iniC)
        self.__contr = Controller(self.__p)
        
    def findPathDFS(self):
        startClock = time()
        print(str(self.__contr.DFS(self.__p.getRoot())))
        print('Execution time: ', time() - startClock, " seconds")
        
    def findPathGreedy(self):
        startClock = time()
        print(str(self.__contr.Greedy(self.__p.getRoot())))
        print("Execution time: ", time() - startClock, " seconds")
        
    def run(self):
        runM = True
        #s = State()
        #c = Configuration([1,3,0,2])
        #p = Problem(c)
        #s += c
        #print(c.getSize())
        #print(p.heuristics(s))
        #for x in p.expand(s):
          #  print(x)
        self.printMainMenu()
        while runM:
            try:
                command = int(input(">>"))
                if command == 0:
                    runM = False
                elif command == 1:
                    self.readConfigSubmenu()
                elif command == 2:
                    self.findPathDFS()
                elif command == 3:
                    self.findPathGreedy()
            except OSError as err:
                print("OS error: {0}".format(err))
def main():
    ui = UI()
    ui.run()
    
main()
        