import numpy as np


class NeuralNetwork:

    def __init__(self, x, y, hidden):
        self.input = x  #(len,5)
        self.weights1 = np.random.rand(self.input.shape[1], hidden) #(5,5)
        self.weights2 = np.random.rand(hidden, 1) #(5,1)
        self.y = y  #(len,1)
        self.output = np.zeros(self.y.shape) #(len,1)
        self.loss = []

    # the function that computs the output of the network for some input
    def feedforward(self):
        self.layer1 = self.linear(np.dot(self.input, self.weights1))
        self.output = self.linear(np.dot(self.layer1, self.weights2))

    # the backpropagation algorithm
    def backprop(self, l_rate):
        # application of the chain rule to find derivative of the
        # loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2 * (self.y - self.output) *
                                            self.linear_derivative(self.output)))

        d_weights1 = np.dot(self.input.T, (np.dot(2 * (self.y -
                                                       self.output) * self.linear_derivative(self.output),
                                                  self.weights2.T) *
                                           self.linear_derivative(self.layer1)))
        # update the weights with the derivative (slope) of the loss function

        self.weights1 += l_rate * d_weights1
        self.weights2 += l_rate * d_weights2
        self.loss.append(sum((self.y - self.output) ** 2))

    # the activation function:
    def linear(self, x):
        return 1 * x + 0.9

    # the derivate of te activation function
    def linear_derivative(self, x):
        return 1

    def compute_loss(self, x, y):
        return sum((x - y) ** 2)
