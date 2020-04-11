from random import randint, random

import numpy


class Ant:

    def __init__(self, size):
        self.size = size * size
        self.n = size
        self.nodes = []
        for i in range(self.n, self.size + self.n):
            self.nodes.append(i)
        self.solution = []
        # initially my solution will look like this
        # [x]
        """
        n = 3
        x = a / n
        y = a / n + a % n
        a    x  y
        3    1  1
        4    1  2 
        5    1  3
        6    2  1
        7    2  2
        8    2  3
        9    3  1
        10   3  2
        11   3  3
        """
        # allocate ant to a random first node

        firstNode = randint(self.n, ((self.n ** 2) + self.n - 1))
        self.solution.append(firstNode)

    def setSolution(self, sol):
        self.solution.clear()
        for s in sol:
            self.solution.append(s)

    def nextMoves(self):
        # possible move from a
        new = []
        for node in self.nodes:
            if node not in self.solution:
                if self.distMove(node - self.n) == 1.0:
                    new.append(node)
        return new

    def distMove(self, a):
        dummy = Ant(self.n)
        dummy.setSolution(self.solution)
        dummy.solution.append(a + self.n)
        return dummy.evaluate()

    def evaluate(self):
        # for every line column it will create a frequency for the elements
        # for every line and column that does not have duplicates it will add 1
        # if a line or column is not filled yet it will automatically be counted
        # if everything is ok 4n
        # we divide by 4n to get the fitness

        fit = 4 * self.n

        # transform solution from list to matrix of pairs s, t
        count = 0
        matrix = []
        for i in range(0, self.n):
            row = []
            for j in range(0, self.n):
                if count < len(self.solution):
                    a = self.solution[count]

                    x = 1
                    if a >= self.n:
                        x = int(a / self.n)
                    y = int(a % self.n) + 1

                    row.append([x, y])
                    count += 1
                else:
                    row.append([0, 0])
                    count += 1
            matrix.append(row)

        # calculate fitness

        for i in range(0, self.n):
            row_one_freq = {}
            row_two_freq = {}
            col_one_freq = {}
            col_two_freq = {}
            for j in range(0, self.n):
                if matrix[i][j][0] not in row_one_freq.keys():
                    row_one_freq[matrix[i][j][0]] = 1
                else:
                    row_one_freq[matrix[i][j][0]] += 1

                if matrix[i][j][1] not in row_two_freq.keys():
                    row_two_freq[matrix[i][j][1]] = 1
                else:
                    row_two_freq[matrix[i][j][1]] += 1

                if matrix[j][i][0] not in col_one_freq.keys():
                    col_one_freq[matrix[j][i][0]] = 1
                else:
                    col_one_freq[matrix[j][i][0]] += 1

                if matrix[j][i][1] not in col_two_freq.keys():
                    col_two_freq[matrix[j][i][1]] = 1
                else:
                    col_two_freq[matrix[j][i][1]] += 1

            for k in row_one_freq.keys():
                if k != 0 and row_one_freq[k] > 1:
                    fit -= 1
                    break

            for k in row_two_freq.keys():
                if k != 0 and row_two_freq[k] > 1:
                    fit -= 1
                    break

            for k in col_one_freq.keys():
                if k != 0 and col_one_freq[k] > 1:
                    fit -= 1
                    break

            for k in col_two_freq.keys():
                if k != 0 and col_two_freq[k] > 1:
                    fit -= 1
                    break

        return fit / (4 * self.n)

    def update(self, q0, trace, alpha, beta):
        nextSteps = []

        for i in self.nextMoves():
            nextSteps.append(i - self.n)

        if len(nextSteps) == 0:
            return False

        p = [[i, self.distMove(i)] for i in nextSteps]

        pr = []

        for i in range(len(p)):
            pr.append([p[i][0] + self.n, (p[i][1] ** beta) * (trace[self.solution[-1] - self.n][i] ** alpha)])

        if random() < q0:
            m = max(pr, key=lambda a: a[1])
            self.solution.append(m[0])
        else:
            s = 0
            for i in range(len(pr)):
                s += pr[i][1]


            rand = numpy.random.uniform(0, s)

            rul = 0
            for p in pr:
                rul += p[1]
                if rul > rand:
                    self.solution.append(p[0])
                    break
        return True

    def fitness(self):
        return self.n * self.n - len(self.solution)
