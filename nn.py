import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        # TODO (Implement FCNNs architecture here)
        # there is a weights matrix(s*f) and a bias vector(s*1) between every two layer (f: first layer, s: second layer) 
        self.weights = []
        self.biases = []
        f = layer_sizes[0]
        for i in range(1, len(layer_sizes)):
            s = layer_sizes[i]
            layer_weights = np.random.standard_normal(size=(s, f))
            self.weights.append(layer_weights)
            layer_biases = np.random.standard_normal(size=(s, 1))
            self.biases.append(layer_biases)
            f = s

    def activation(self, x):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        # TODO (Implement activation function here)
        ## Sigmoid
        return 1 / (1 + np.exp(-x))

        ## ReLU
        return np.where(x < 0, 0, x)

        ## Leaky ReLU
        return np.where(x < 0, -0.001 * x, x)

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # TODO (Implement forward function here)
        temp = x
        for i in range(len(self.weights)):
            z = np.add(self.weights[i].dot(temp), self.biases[i])
            temp = self.activation(z)
        return temp
