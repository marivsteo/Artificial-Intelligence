import random

import numpy as np


class Evolutionary:
    def __init__(self, size):
        self.size = size

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


    def getSize(self):
        return self.size

    def getPermutation(self, n):
        ordered = []
        for i in range(1, n + 1):
            ordered.append(i)
        return np.random.permutation(ordered)

    def createIndividual(self, n):
        return [self.getPermutation(n) for i in range(n * 2)]

    def createPopulation(self, pop, n):
        return [self.createIndividual(n) for i in range(pop)]

    def crossover(self, parent1, parent2):
        progeny = []
        for i in range(len(parent1)):
            if random.randint(0, 1) % 2 == 0:
                progeny.append(parent2[i])
            else:
                progeny.append(parent1[i])
        return progeny

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

    def mutate(self, child, probability):
        if probability > random.uniform(0, 1):
            randomPos = random.randrange(0, len(child))
            child[randomPos] = self.getPermutation(len(child) // 2)
        return child

    def getFittest(self, pop):
        minF = 100000
        minI = []
        for i in range(len(pop)):
            if self.fitness(pop[i]) < minF:
                minF = self.fitness(pop[i])
                minI = pop[i]
        return minI

    def getMinFitness(self, pop):
        minF = 100000
        for i in range(len(pop)):
            if self.fitness(pop[i]) < minF:
                minF = self.fitness(pop[i])
        return minF

    def sumFitness(self, pop):
        sum = 0
        for i in range(len(pop)):
            sum = sum + self.fitness(pop[i])
        return sum

    def iterationEA(self, pop, mutation):
        parent1 = random.randrange(0, len(pop) - 1)
        parent2 = random.randrange(0, len(pop) - 1)
        if parent1 != parent2:
            child = self.crossover(pop[parent1], pop[parent2])
            child = self.mutate(child, mutation)
            f1 = self.fitness(pop[parent1])
            f2 = self.fitness(pop[parent2])
            fc = self.fitness(child)
            if f1 > f2 and f1 > fc:
                pop[parent1] = child
            if f2 > f1 and f2 > fc:
                pop[parent2] = child
        return pop
