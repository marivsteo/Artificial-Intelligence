import pandas as pd
import random

dataset = pd.read_csv("C:/Users/Marius/Desktop/university 2/SEM2/ArtInt/Assignments/lab07/Files/database", sep=' ', header=None)


class Controller:

    def __init__(self, size, learning_rate):
        self.weights = self.initial_weights(size)
        self.size = size
        self.learning_rate = learning_rate

    def initial_weights(self, length):
        weights = []
        for x in range(length):
            weights.append(random.randint(-10, 10))
        return weights

    def linear_function(self, weights):
        total = self.weights[-1]
        for index in range(self.size - 1):
            # print(str(self.weights[index]) + ' * ' + str(weights[index]))
            total = total + self.weights[index] * weights[index]
        return total

    def error(self, weights):
        return abs(weights[self.size - 1] - self.linear_function(weights))

    def total_error(self):
        err = 0
        for index, row in dataset.iterrows():
            err += self.error(row) ** 2
        return err / float(len(dataset.index))

    def step(self):
        gradient = [0 for i in range(self.size)]
        nr = float(len(dataset.index))

        for idx, row in dataset.iterrows():
            y = row[self.size - 1]
            value = self.linear_function(row)

            for i in range(self.size - 1):
                gradient[i] += -(2 / nr) * row[i] * (y - value)

            gradient[self.size - 1] += -(2 / nr) * (y - value)

        for i in range(self.size):
            self.weights[i] = self.weights[i] - (self.learning_rate * gradient[i])

    def print_weights(self):
        print("The final weights: ", self.weights)
