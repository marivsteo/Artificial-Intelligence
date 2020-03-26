from ParticleSwarmUseless.Domain import PSO


class PSOController:

    def __init__(self, n):
        self.pso = PSO(n)

    def solve(self, iterations, particles, n):
        w = 1.0
        c1 = 1.
        c2 = 2.5
        sizeOfNeighbourhood = 20

        P = self.pso.createParticlesPopulation(particles, n)

        neighbourhoods = self.pso.selectNeighbors(P, sizeOfNeighbourhood)

        for i in range(iterations):
            P = self.pso.iteration(P, neighbourhoods, c1, c2, w / (i + 1))

        # print the best individual
        best = 0
        for i in range(1, len(P)):
            if (P[i].fitness < P[best].fitness):
                best = i

        fitnessOptim = P[best].fitness
        individualOptim = P[best].pozition
        print(fitnessOptim)
        P[best].printSquares(individualOptim)
