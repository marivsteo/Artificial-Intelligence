import numpy
import matplotlib.pyplot as plt
from Evolutionary.Domain import Evolutionary


class EAController:

    def __init__(self, n):
        self.evo = Evolutionary(n)

    def solve(self, population, iterations, mutation, n):
        size = self.evo.getSize()
        population = self.evo.createPopulation(population, n)
        for i in range(iterations):
            population = self.evo.iterationEA(population, mutation)

        str1 = "Fitness is: " + str(self.evo.getMinFitness(population)) + "\n"
        str1 += self.evo.printSquares(self.evo.getFittest(population))

        x = numpy.array([self.evo.fitness(population[x]) for x in range(len(population))])
        y = numpy.array([x for x in range(len(population))])

        # e = numpy.array(x for x in range (4))
        plt.plot(y, x)
        plt.show()

        return str1