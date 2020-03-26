import numpy
import numpy as np
import random
import matplotlib.pyplot as plt


class Particle:

    def __init__(self, n):

        self._position = self.createIndividual(n)
        self.evaluate()
        self.velocity = [0 for i in range(n)]

        # the memory of that particle
        self._bestPosition = self._position.copy()
        self._bestFitness = self._fitness

    def createIndividual(self, n):
        return [self.getPermutation(n) for i in range(n * 2)]

    def getPermutation(self, n):
        ordered = []
        for i in range(1, n + 1):
            ordered.append(i)
        return np.random.permutation(ordered)

    def printSquares(self, individual):
        str1 = ''
        half = len(individual) // 2
        A, B = individual[:half], individual[half:]
        for i in range(half):
            for j in range(half):
                # str1 += str(A[i][j]) + ", " + str(B[i][j]) + "   "
                str1 += "(" + str(A[i][j]) + ", " + str(B[i][j]) + ")" + " "
            str1 += "\n"
        print(str1)

    def fitnesses(self, individual):
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

    def fit(self, position):

        return self.fitnesses(position)

    def evaluate(self):

        self._fitness = self.fit(self._position)

    @property
    def position(self):
        return self._position

    @property
    def fitness(self):
        return self._fitness

    @property
    def bestPosition(self):
        return self._bestPosition

    @property
    def bestFitness(self):
        return self._bestFitness

    @position.setter
    def position(self, newPosition):
        self._position = newPosition.copy()
        # automatic evaluation of particle's fitness
        self.evaluate()
        # automatic update of particle's memory
        if (self._fitness < self._bestFitness):
            self._bestPosition = self._position
            self._bestFitness = self._fitness


class PSO:

    def __init__(self, n):
        self.size = n

    def createParticlesPopulation(self, pop, n):
        return [Particle(n) for i in range(pop)]

    def selectNeighbors(self, pop, nSize):

        if (nSize > len(pop)):
            nSize = len(pop)

        # Attention if nSize==len(pop) this selection is not a proper one
        # use a different approach (like shuffle to form a permutation)
        neighbors = []
        for i in range(len(pop)):
            local_neighbor = []
            for j in range(nSize):
                x = random.randint(0, len(pop) - 1)
                while x in local_neighbor:
                    x = random.randint(0, len(pop) - 1)
                local_neighbor.append(x)
            neighbors.append(local_neighbor.copy())
        return neighbors

    

    def iteration(self, population, neighbours, c1, c2, w):

        bestNeighbors = []
        # determine the best neighbor for each particle
        for i in range(len(population)):
            bestNeighbors.append(neighbours[i][0])
            for j in range(1, len(neighbours[i])):
                if (population[bestNeighbors[i]].fitness > population[neighbours[i][j]].fitness):
                    bestNeighbors[i] = neighbours[i][j]

        # update the velocity for each particle
        for i in range(len(population)):
            for j in range(len(population[0].velocity)):
                newVelocity = w * population[i].velocity[j]
                newVelocity = newVelocity + c1 * random.random() * (
                            population[bestNeighbors[i]].position[j] - population[i].position[j])
                newVelocity = newVelocity + c2 * random.random() * (
                            population[i].bestPosition[j] - population[i].position[j])
                population[i].velocity[j] = newVelocity

        for i in range(len(population)):
            newPosition = []
            for j in range(len(population[0].velocity)):
                newPosition.append(population[i].position[j] + population[i].velocity[j])
            population[i].position = newPosition
        return population

    result = []
    finalFitness = []

    def mainPSO(self, iterations, n, nrparticles):
        # specific parameters for PSO
        w = 1.0
        c1 = 1.
        c2 = 2.5
        sizeOfNeighbourhood = 20

        population = self.createParticlesPopulation(nrparticles, n)

        # we establish the particles' neighbors
        neighbourhoods = self.selectNeighbors(population, sizeOfNeighbourhood)

        for i in range(iterations):
            population = self.iteration(population, neighbourhoods, c1, c2, w / (i + 1))

        # print the best individual
        # best = 0
        # for i in range(1, len(population)):
        #     if (population[i].fitness < population[best].fitness):
        #         best = i

        # global result
        # global finalFitness

        for i in population:
            i.printSquares(i.position)

        best = population[0]
        for i in population:
            if i.fitness < best.fitness:
                best = i

        fitnessOptim = best.fitness
        individualOptim = best.position
        #finalFitness.append(str(fitnessOptim))
        print("Result fitness: " + str(fitnessOptim) + "\n")

        best.printSquares(best._bestPosition)
        #result.append(individualOptim)

        x = numpy.array([population[x].fitness for x in range(len(population))])
        y = numpy.array([x for x in range(len(population))])
        plt.plot(y, x)
        plt.show()
                # print('Result: The detectet minimum point is (%3.2f %3.2f) \n with function\'s value %3.2f'% \
        #      (individualOptim[0],individualOptim[1], fitnessOptim) )


