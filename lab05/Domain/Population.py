from Domain.Ant import Ant


class Population:

    def __init__(self, populationSize, solutionSize):
        self.antSet = []

        for i in range(populationSize):
            self.antSet.append(Ant(solutionSize))

    def getAntSet(self):
        return self.antSet

    def getSize(self):
        return len(self.antSet)
