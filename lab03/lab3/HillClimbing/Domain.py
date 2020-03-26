import copy
import numpy as np


class HC:

    def __init__(self, n):
        self.size = n

    def printSquares(self, individual):
        str1 = ''
        half = len(individual) // 2
        A, B = individual[:half], individual[half:]
        for i in range(half):
            for j in range(half):
                # str1 += str(A[i][j]) + ", " + str(B[i][j]) + "   "
                str1 += "(" + str(A[i][j]) + ", " + str(B[i][j]) + ")" + " "
            str1 += "\n"
        return str1

    def getPermutation(self, n):
        ordered = []
        for i in range(1, n + 1):
            ordered.append(i)
        return np.random.permutation(ordered)

    def createIndividual(self, n):
        return [self.getPermutation(n) for i in range(n * 2)]

    def permutation(self, lst):

        if len(lst) == 0:
            return []

        if len(lst) == 1:
            return [lst]

        l = []
        for i in range(len(lst)):
            m = lst[i]

            remLst = lst[:i] + lst[i + 1:]

            for p in self.permutation(remLst):
                l.append([m] + p)
        return l

    def getAllPermutations(self, n):
        ordered = []
        for i in range(1, n + 1):
            ordered.append(i)
        return self.permutation(ordered)

    def getNeighbours(self, individual, permutations):
        neighbours = []
        for permutation in range(len(permutations)):
            for i in range(len(individual)):
                auxiliary = copy.deepcopy(individual)
                auxiliary[i] = permutations[permutation]
                neighbours.append(auxiliary)
        return neighbours

    def iterationHC(self, individual, permutations):
        vecinity = self.getNeighbours(individual, permutations)
        fittest = self.getFittest(vecinity)
        if self.fitness(fittest) < self.fitness(individual):
            return fittest
        else:
            return individual

    def fitness(self, individual):
        count1 = 0
        count2 = 0
        count3 = 0

        for j in range(len(individual) // 2):
            visited = []
            for i in range(len(individual) // 2):
                if individual[i][j] in visited:
                    count1 += 1
                visited.append(individual[i][j])

        for j in range(len(individual) // 2):
            visited = []
            for i in range(len(individual) // 2, len(individual)):
                if individual[i][j] in visited:
                    count2 += 1
                visited.append(individual[i][j])

        pairs = []
        for j in range(len(individual) // 2):
            for i in range(len(individual) // 2):
                pairs.append((individual[i][j], individual[i + len(individual) // 2][j]))

        count3 = (len(individual) // 2 * len(individual) // 2 * -1)
        for pair1 in pairs:
            for pair2 in pairs:
                if pair1 == pair2:
                    count3 += 1

        return count1 + count2 + count3

    def getFittest(self, pop):
        minF = 100000
        minI = []
        for i in range(len(pop)):
            if self.fitness(pop[i]) < minF:
                minF = self.fitness(pop[i])
                minI = pop[i]
        return minI

    def mainHC(self, iterations, n):
        individual = self.createIndividual(n)
        permutations = self.getAllPermutations(n)
        for i in range(iterations):
            individual = self.iterationHC(individual, permutations)
        print("The minimum fitness = " + str(self.fitness(individual)))
        self.printSquares(individual)

        # self.sw.setWindowTitle("Best solution")

        # centralWidget = QWidget(self.sw)
        # w.setCentralWidget(centralWidget)

        # gridLayout = QGridLayout(self.sw)
        # centralWidget.setLayout(gridLayout)

        # self.sw.setMinimumSize(QSize(200, 200))
        # self.sw.setMaximumSize(QSize(200, 200))

        # title = QLabel("The minimum fitness = " + str(super().fitness(individual)) + "\n" +
                      # str(super().printSquares(individual)), self.sw)
        # title.setAlignment(QtCore.Qt.AlignCenter)
        # gridLayout.addWidget(title, 0, 0)

        # self.sw.show()

        # return self.fitness(individual)

    def getSize(self):
        return self.size