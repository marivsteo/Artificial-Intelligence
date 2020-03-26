from ParticleSwarm.board import Board
from random import randint, random
from operator import add
from math import sin, pow
from itertools import *
from ParticleSwarm.validator import Validator
import numpy
import matplotlib.pyplot as plt


class particle:
    def __init__(self, l):
        self.validator = Validator(l)

        matrix = []
        for i in range(l):
            line = []
            for j in range(l):
                line.append((randint(1, l), randint(1, l)))
            matrix.append(line)

        self.position = matrix
        self.evaluate()
        self.velocity = [0 for i in range(l)]

        self.bestposition = self.position.copy()
        self.bestFitness = self.fitness

    def fit(self, individual):
        fit = 3
        if self.validator.lineCheck(individual):
            fit = fit - 1
        if self.validator.columnCheck(individual):
            fit = fit - 1
        if self.validator.dublicatesCheck(individual):
            fit = fit - 1
        return fit

    def evaluate(self):
        self.fitness = self.fit(self.position)


def population(l, dimIndivid):
    pop = []
    for i in range(l):
        pop.append(particle(dimIndivid))
    return pop


def selectNeighbors(pop, nSize):
    if (nSize > len(pop)):
        nSize = len(pop)
    neighbors = []
    for i in range(len(pop)):
        localNeighbor = []
        for j in range(nSize):
            x = randint(0, len(pop) - 1)
            while (x in localNeighbor):
                x = randint(0, len(pop) - 1)
            localNeighbor.append(x)
        neighbors.append(localNeighbor.copy())
    return neighbors


def formBoard(p, n):
    board = Board(n).board
    for i in range(n):
        for j in range(n):
            board[i][j] = (p[i][j], p[i + n][j])
    return board


def iteration(pop, neighbors, c1, c2, w):
    bestNeighbors = []
    # find best neighbor
    for i in range(len(pop)):
        bestNeighbors.append(neighbors[i][0])
        for j in range(1, len(neighbors[i])):
            if (pop[bestNeighbors[i]].fitness > pop[neighbors[i][j]].fitness):
                bestNeighbors[i] = neighbors[i][j]

    # update velocity
    for i in range(len(pop)):
        for j in range(len(pop[0].velocity)):
            newVelocity = w * pop[i].velocity[j]
            for p in range(len(pop[0].position[0])):
                for q in range(len(pop[0].position[0][0])):
                    newVelocity = newVelocity + c1 * random() * (
                                pop[bestNeighbors[i]].position[j][p][q] - pop[i].position[j][p][q])
                    newVelocity = newVelocity + c2 * random() * (
                                pop[i].bestposition[j][p][q] - pop[i].position[j][p][q])
            pop[i].velocity[j] = newVelocity

    # update position
    for i in range(len(pop)):
        newposition = []
        for j in range(len(pop[0].velocity)):
            newposition.append(pop[i].position[j])
        pop[i].position = newposition
        pop[i].evaluate()
    return pop


def solvePSO(noIteratii, nrparticles, size, w_, c1_, c2_):
    n = size
    dimParticle = n
    w = w_
    c1 = c1_
    c2 = c2_
    sizeOfNeighborhood = 40
    pop = population(nrparticles, n)
    neighborhoods = selectNeighbors(pop, sizeOfNeighborhood)

    for i in range(noIteratii):
        pop = iteration(pop, neighborhoods, c1, c2, w / (i + 1))
    global outcome
    global outcomeFitness
    best = pop[0]
    for i in pop:
        if i.fitness < best.fitness:
            best = i

    fitnessOptim = best.fitness
    individualOptim = best.position
    outcomeFitness.append(str(fitnessOptim))

    str1 = ''

    str1 += "Result: \n"
    for i in individualOptim:
        str1 += str(i)
    str1 += "\n Results fitness: " + str(fitnessOptim) + "\n"

    outcome.append(individualOptim)

    if fitnessOptim > 0:
        str1 += "\n" + "No solution found"

    print(str1)

    x = numpy.array([pop[x].fitness for x in range(len(pop))])
    y = numpy.array([x for x in range(len(pop))])
    plt.plot(y, x)
    plt.show()

    # return str1


outcome = []
outcomeFitness = []
