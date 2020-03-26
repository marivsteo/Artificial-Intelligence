from HillClimbing.Domain import HC

class HCController:

    def __init__(self, n):
        self.evo = HC(n)
        self.result = ''

    def solve(self, iterations, n):
        individual = self.evo.createIndividual(n)
        permutations = self.evo.getAllPermutations(n)
        for i in range(iterations):
            individual = self.evo.iterationHC(individual, permutations)

        str1 = "Min fitness: " + str(self.evo.fitness(individual)) + "\n"
        str1 += self.evo.printSquares(individual)

        self.result = str1