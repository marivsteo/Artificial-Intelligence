import numpy
import matplotlib.pyplot as plt
from Controller.Controller import Controller
from Domain.Ant import Ant


class Problem:

    def __init__(self):
        self.loadProblem()
        self.controller = Controller(self.noAnts, self.antSize)

    def loadProblem(self):
        f = open("input.txt", "r")
        self.antSize = int(f.readline())
        self.noEpoch = int(f.readline())
        self.noAnts = int(f.readline())
        self.alpha = float(f.readline())  # trail importance
        self.beta = float(f.readline())  # visibility importance
        self.rho = float(f.readline())  # pheromone degradation coefficient
        self.q0 = float(f.readline())  # initial value of pheromone

    def run(self):
        bestAnt = Ant(self.antSize)
        bestAnt.setSolution([])

        for i in range(self.noEpoch):
            ant = self.controller.iteration(self.q0, self.alpha, self.beta, self.rho)
            if ant.fitness() < bestAnt.fitness():
                bestAnt.setSolution(ant.solution)
                if bestAnt.fitness() == 0:
                    break

        print("Best found path: " + str(bestAnt.solution))
        n = bestAnt.solution
        count = 0
        matrix = []
        for i in range(self.antSize):
            row = []
            for j in range(self.antSize):
                x = 1
                if count < len(n):
                    if n[count] >= self.antSize:
                        x = int(n[count] / self.antSize)
                    y = int(n[count] % self.antSize) + 1
                else:
                    x = 0
                    y = 0
                row.append([x, y])
                count += 1
            matrix.append(row)

        print("Best found solution: ")
        for i in range(len(matrix)):
            print(matrix[i])
        print("Fitness: " + str(bestAnt.fitness()))

    def test(self):
        fitness = []
        for j in range(0, 30):
            bestAnt = Ant(self.antSize)
            bestAnt.setSolution([])

            for i in range(self.noEpoch):
                ant = self.controller.iteration(self.q0, self.alpha, self.beta, self.rho)
                fitness.append(ant.fitness())
                if ant.fitness() < bestAnt.fitness():
                    bestAnt.setSolution(ant.solution)
                    if bestAnt.fitness() == 0:
                        break

            # fitness.append(bestAnt.fitness())

        result = "Average: " + str(numpy.average(fitness)) + "\n" + "Standard deviation: " + str(numpy.std(fitness))
        print(result)
        plt.plot(fitness)
        plt.show()

def printTheMenu():
    print("\t 1 - Find solutions")
    print("\t 2 - See statistics")
    print("\t 0 - exit")

def main():
    p = Problem()

    choice = -1
    while choice != 0:
        printTheMenu()
        choice = int(input(">>"))

        if choice == 1:
            p.run()
        elif choice == 2:
            p.test()
        elif choice == 0:
            print("Endgame")
        else:
            print("Not a valid option")

main()