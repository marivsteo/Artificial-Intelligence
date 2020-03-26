from time import time

from Evolutionary.Controller import EAController
from HillClimbing.Controller import HCController
from ParticleSwarm.PSOv2 import *


class UI:
    def __init__(self):
        self.__particle = 1000
        self.__size = 3
        self.__pop = 25
        self.__iter = 500
        self.__mut = 0.5

    def printMainMenu(self):
        s = ''
        s += "The default size of the square is 3\n"
        s += "0 - exit \n"
        s += "1 - read size of square \n"
        s += "2 - find solution with EA \n"
        s += "3 - find solution with HC  \n"
        s += "4 - find solution with PSO \n"
        print(s)

    def readConfigSubmenu(self):
        n = 3
        try:
            print("Input size of square (implicit = 3)")
            n = int(input("size = "))
        except:
            print("This is not a number. The size of the square is still 3")
            n = 3
        self.__size = n

    def readConfigSubmenuEA(self):
        try:
            print("Input the population size")
            pop = int(input("population = "))
            print("Input number of iterations")
            it = int(input("iterations = "))
            print("Input the probability of mutation (between 0 and 1)")
            mut = float(input("mutation = "))
        except:
            print("Some numbers are invalid. Parameters set to default\n Population = 25\n Iterations = 500\n Mutation = 0.5")
            pop = 25
            it = 500
            mut = 0.5
        self.__pop = pop
        self.__iter = it
        self.__mut = mut

    def readConfigSubmenuHC(self):
        try:
            print("Input the number of iterations")
            it = int(input("iterations = "))
        except:
            print("Invalid number of iterations. Default is 500.")
            it = 500
        self.__it = it

    def readConfigSubmenuPSO(self):
        try:
            print("Input number of iterations")
            it = int(input("iterations = "))
            print("Input the particle number")
            par = int(input("particles = "))
        except:
            print("Some numbers are invalid. Parameters set to default")
            it = 500
            par = 1000
        self.__iter = it
        self.__particle = par

    def findSolEA(self):
        startClock = time()
        controller = EAController(self.__size)
        controller.solve(self.__pop, self.__iter, self.__mut, self.__size)
        print('Execution time: ', time() - startClock, " seconds")

    def findSolHC(self):
        startClock = time()
        controller = HCController(self.__size)
        controller.solve(self.__iter, self.__size)
        print("Execution time: ", time() - startClock, " seconds")

    def findSolPSO(self):
        startClock = time()
        solvePSO(self.__iter, self.__particle, self.__size)
        # pid = threading.Thread(target=first, args=(int(100), self.number,))
        # pid.start()
        # self.table.setWordWrap(True)
        matrix = ""
        for i in range(self.__size):
            for j in range(self.__size):
                matrix = matrix + str(outcome[0][i][j]) + " "
            matrix = matrix + "\n"
        # self.table.text = "dfikguifgl'zkxcfhfvufkuifgsadghfguisdfyfgyshd"
        # string = "detected minimum : " + str(outcomeFitness[0]) + "\n" + str(matrix)
        print("Execution time: ", time() - startClock, " seconds")

    def run(self):
        runs = True
        self.printMainMenu()
        while runs:
            try:
                command = int(input(">>"))
                if command == 0:
                    runs = False
                elif command == 1:
                    self.readConfigSubmenu()
                elif command == 2:
                    self.readConfigSubmenuEA()
                    self.findSolEA()
                elif command == 3:
                    self.readConfigSubmenuHC()
                    self.findSolHC()
                elif command == 4:
                    self.readConfigSubmenuPSO()
                    self.findSolPSO()
            except OSError as err:
                print("OS error: {0}".format(err))
