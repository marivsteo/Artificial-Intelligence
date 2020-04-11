from Domain.Population import Population


class Controller:

    def __init__(self, populationSize, solutionSize):
        self.populationSize = populationSize
        self.sol = solutionSize
        self.trace = []
        for i in range(solutionSize * solutionSize):
            row = []
            for j in range(solutionSize * solutionSize):
                row.append(1)
            self.trace.append(row)

    def iteration(self, q0, alpha, beta, rho):
        self.population = Population(self.populationSize, self.sol)
        antSet = self.population.getAntSet()

        for k in range(1, self.sol * self.sol):
            for x in antSet:
                x.update(q0, self.trace, alpha, beta)

                dTrace = []
                for i in range(len(antSet)):
                    if antSet[i].fitness() == 0:
                        dTrace.append(1.0)
                    else:
                        dTrace.append(1.0 / antSet[i].fitness())

                for i in range(self.sol * self.sol):
                    for j in range(self.sol * self.sol):
                        self.trace[i][j] = (1 - rho) * self.trace[i][j]

                for i in range(len(antSet)):
                    for j in range(len(antSet[i].solution) - 1):
                        x = antSet[i].solution[j] - self.sol
                        y = antSet[i].solution[j + 1] - self.sol
                        self.trace[x][y] = self.trace[x][y] + dTrace[i]



        f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
        f = max(f, key=lambda a: a[0])

        dTrace = 0.01
        if antSet[f[1]].evaluate() != 0.0:
            dTrace = 1.0 / antSet[f[1]].evaluate()

        for j in range(len(antSet[f[1]].solution) - 1):
            x = antSet[f[1]].solution[j] - self.sol
            y = antSet[f[1]].solution[j + 1] - self.sol
            self.trace[x][y] = self.trace[x][y] + dTrace

        f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
        f = max(f, key=lambda a: a[0])
        return antSet[f[1]]



