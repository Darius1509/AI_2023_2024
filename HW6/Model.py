import numpy
from Layer import Layer
from sklearn import metrics
import matplotlib.pyplot as plt

class Model:
    def __init__(self, network: Layer, loss_function="cross_entropy"):
        self.network = network
        self.loss_function = loss_function
        self.errors = []
        if loss_function == "cross_entropy":
            self.loss_function = Model.cross_entropy_loss
        elif loss_function == "square_loss":
            self.loss_function = Model.square_loss

    def get_vectorized_target(self, target, dimension):
        vectorized_target = numpy.zeros((dimension,target.shape[0]))
        for i in range(target.shape[0]):
            vectorized_target[target[i]][i] = 1
        return vectorized_target

    def square_loss(self, predicted, target):
        target = self.get_vectorized_target(target, dimension=predicted.shape[1])
        return numpy.sum(numpy.square(predicted - target.T)) * 1/predicted.shape[0]

    def cross_entropy_loss(self,predicted, target):
        target = self.get_vectorized_target(target, dimension=predicted.shape[1])
        sum = numpy.log(predicted) @ target
        sum = numpy.sum(sum)
        return sum

    def fit(self, X_set, Y_set, epochs, learning_rate, batch_size):
        for epoch in range(epochs):
            for batch_i in range(len(X_set) // batch_size):
                X_batch, y_batch = X_set[batch_size * batch_i:batch_size * (batch_i + 1), :], Y_set[batch_size * batch_i:batch_size * (batch_i + 1)]
                output = self.network(X_batch)
                error = self.loss_function(self,output, y_batch)
                self.network.back_propagation(error, y_batch, learning_rate, batch_size)
            self.errors.append(error)
            #print(f"Epoch: {epoch}  Error: {error}")

    def predict(self, test_set):
        return self.network(test_set)

    def get_dominant_answer(self, output):
        return numpy.argmax(output, axis=1)

    def evaluate(self, test_set, test_labels):
        output = self.get_dominant_answer(self.predict(test_set))
        error = output != test_labels
        return numpy.sum(error) / len(error)

    def accuracy(self, test_set, test_labels):
        print("Accuracy: ", numpy.sum(self.get_dominant_answer(self.predict(test_set)) == test_labels) / test_labels.shape[0])

    def plot_error(self):
        #set plt bounds y to [0,1]
        plt.plot(self.errors)
        plt.xlabel("Epoch")
        plt.ylabel("Error")
        plt.ylim(0, 1.5)
        plt.show()

    def plot_wrong_classified(self, test_set, test_labels):
        output = self.get_dominant_answer(self.predict(test_set))
        wrong_classified = []
        for i in range(test_labels.shape[0]):
            if output[i] != test_labels[i]:
                wrong_classified.append(test_set[i])
        wrong_classified = numpy.array(wrong_classified)
        plt.scatter(wrong_classified[:,0], wrong_classified[:,1], c="red")
        plt.xlabel("sepal_length")
        plt.ylabel("sepal_width")
        plt.show()

    def confusion_matrix(self, test_set, test_labels):
        output = self.get_dominant_answer(self.predict(test_set))
        confusion_matrix = numpy.zeros((2, test_labels.shape[0]))
        for i in range(test_labels.shape[0]):
            confusion_matrix[1][i] = test_labels[i]
            confusion_matrix[0][i] = output[i]
        print("Confusion Matrix: ", confusion_matrix)
        return confusion_matrix

    def plot_confusion_matrix(self, test_set, target, title='Test set'):
        predicted = self.get_dominant_answer(self.predict(test_set))
        confusion_matrix = metrics.confusion_matrix(target, predicted)
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix)
        cm_display.plot()
        plt.show()