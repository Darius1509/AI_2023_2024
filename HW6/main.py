import pandas
import time
from Layer import Layer
from Model import Model
from sklearn.model_selection import train_test_split
import numpy

seeds_data = pandas.read_csv('seeds_dataset.csv', names=['Attr1', 'Attr2', 'Attr3', 'Attr4', 'Attr5', 'Attr6', 'Attr7', 'class'])
print(seeds_data)

X = seeds_data[['Attr1', 'Attr2', 'Attr3', 'Attr4', 'Attr5', 'Attr6', 'Attr7']]  # Features
y = seeds_data['class']  # Labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2) # 80% training and 20% test

X_train, X_test, y_train, y_test = X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()

start_time = time.time()

input_neurons = X_train.shape[1]
hidden_neurons = 20
output_neurons = 3
bias = 1
epochs = 100
learning_rate = 0.05
no_batches = 1
batch_size = X_train.shape[0] // no_batches
layer1 = Layer((input_neurons, hidden_neurons),layer_number=1,layer_type="hidden")   # input layer to hidden (7, 20)
network = Layer((hidden_neurons, output_neurons), layer1, activation_function="softmax",layer_number=3, layer_type="output")  # hidden layer to output (20, 4)

model = Model(network, loss_function="square_loss")
# model = Model(network, loss_function="cross_entropy")

y_train_converted = numpy.array([y-1 for y in y_train])

model.fit(X_train,y_train_converted, epochs, learning_rate, batch_size)

predicted = model.predict(X_test)

y_test_converted = numpy.array([y-1 for y in y_test])

print("Error: ",model.evaluate(X_train, y_train_converted))
model.accuracy(X_train, y_train_converted)

print("Error: ",model.evaluate(X_test, y_test_converted))
model.accuracy(X_test, y_test_converted)

print("--- %s seconds ---" % (time.time() - start_time))

model.plot_error()
model.plot_wrong_classified(X_test, y_test_converted)
model.plot_confusion_matrix(X_train, y_train_converted, "Train set")
model.plot_confusion_matrix(X_test, y_test_converted)