import numpy

class Layer:
    def __init__(self, dimensions, previous_layer=None, activation_function="sigmoid", layer_number=1, layer_type="hidden"):
        self.layer_number = layer_number
        self.layer_type = layer_type
        self.dimensions = dimensions
        self.previous_layer = None
        self.ins = None
        self.outs = None

        if previous_layer is not None:
            if previous_layer.dimensions[1] != dimensions[0]:
                raise Exception("Invalid dimensions")
            self.previous_layer = previous_layer
            # self.weights = numpy.random.normal(0,1 / numpy.sqrt(self.dimensions[1]),size=self.dimensions)
            self.weights = numpy.random.randn(self.dimensions[0], self.dimensions[1])
            self.bias = numpy.random.randn(1, self.dimensions[1])
        else:
            # self.weights = numpy.random.normal(0,1 / numpy.sqrt(self.dimensions[1]),size=self.dimensions)
            self.weights = numpy.random.randn(self.dimensions[0], self.dimensions[1])
            self.bias = numpy.random.randn(1, self.dimensions[1])

        if activation_function == "sigmoid":
            self.activation_function = numpy.vectorize(lambda x:  1.0 / (1.0 + numpy.exp(-x)) if (x>=0) else numpy.exp(x) / (1.0 + numpy.exp(x)))
            self.activation_function_derivative = numpy.vectorize(lambda x: self.activation_function(x) * (1 - self.activation_function(x)))
        else:   # softmax
            self.activation_function = self.softmax
            self.activation_function_derivative = lambda x, y: x - y

    # def sigmoid(self, x):
    #     return 1.0 / (1.0 + numpy.exp(-x)) if (x>=0) else numpy.exp(-x) / (1.0 + numpy.exp(-x))
    # def sigmoid_derivative(self, x):
    #     return x * (1 - x)
    # def softmax(self, x):
    #     exps = numpy.exp(x - numpy.max(x))
    #     return exps / numpy.sum(exps)
    def softmax(self, x):
        for i in range(x.shape[0]):
            x[i] = numpy.exp(x[i] - numpy.max(x)) / numpy.sum(numpy.exp(x[i] - numpy.max(x)))
        return x

    def get_vectorized_target(self, target):
        vectorized_target = numpy.zeros(self.outs.shape)
        for i in range(target.shape[0]):
            vectorized_target[i][target[i]] = 1
        return vectorized_target

    def forward_propagation(self, input):
        print(f"Doing forward propagation layer {self.layer_number} to layer {self.layer_number + 1}")
        return input @ self.weights + self.bias

    def gradient_descent(self, gradients_weights, gradients_bias, learning_rate):
        self.weights -= gradients_weights * learning_rate
        self.bias -= gradients_bias * learning_rate

    def back_propagation(self, error,target, learning_rate, batch_size):
        print(f"Doing backpropagation for layer {self.layer_number + 1} to layer {self.layer_number}")
        if self.previous_layer is None:
            delta = self.activation_function_derivative(self.outs) * error / batch_size
            gradients_weights = (delta.T @ self.ins).T
            gradients_bias = numpy.sum(delta,axis=0) / batch_size
            self.gradient_descent(gradients_weights, gradients_bias, learning_rate)

        elif self.layer_type == "output":
            delta = self.activation_function_derivative(self.outs, self.get_vectorized_target(target)) / batch_size
            gradients_weights = (delta.T @ self.previous_layer.outs).T
            gradients_bias = numpy.sum(delta,axis=0) / batch_size
            self.gradient_descent(gradients_weights, gradients_bias, learning_rate)
            error = delta @ self.weights.T
            self.previous_layer.back_propagation(error,target, learning_rate, batch_size)

        else:
            delta = self.activation_function_derivative(self.outs) * error / batch_size
            gradients_weights = (delta.T @ self.previous_layer.outs).T
            gradients_bias = numpy.sum(delta,axis=0) / batch_size
            self.gradient_descent(gradients_weights, gradients_bias, learning_rate)
            error = delta @ self.weights.T
            self.previous_layer.back_propagation(error,target, learning_rate, batch_size)


    def __call__(self, inputs):
        if self.previous_layer is None:
            self.ins = inputs
            self.outs = self.forward_propagation(self.ins)
            return self.activation_function(self.outs)
        else:
            self.ins = self.previous_layer(inputs)
            self.outs = self.forward_propagation(self.ins)
            return self.activation_function(self.outs)