import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

#1
def read_dataset(file_path):
    # citim din dataset
    df = pd.read_csv(file_path, header=None, delim_whitespace=True)
    # amestecam
    df = df.sample(frac=1).reset_index(drop=True)
    # separam training data de test data
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    # extragem features si labels
    training_feat, training_lbl = train_df.iloc[:, :-1], train_df.iloc[:, -1]
    test_feat, test_lbl = test_df.iloc[:, :-1], test_df.iloc[:, -1]
    training_lbl = training_lbl.values.reshape(-1, 1)
    test_lbl = test_lbl.values.reshape(-1, 1)
    # one-hot encoding
    encoder = OneHotEncoder(sparse=False)
    training_lbl_enc = encoder.fit_transform(training_lbl)
    test_lbl_enc = encoder.transform(test_lbl)
    return training_feat.values, training_lbl_enc, test_feat.values, test_lbl_enc

file_path = 'seeds_dataset.txt'
train_features, train_labels, test_features, test_labels = read_dataset(file_path)

#2
def initialize_neural_network():
    np.random.seed(42)
    weights_1 = np.random.uniform(-0.5, 0.5, (4, 7))
    bias_1= np.zeros((4, 1))
    weights_2 = np.random.uniform(-0.5, 0.5, (3, 4))
    bias_2 = np.zeros((3, 1))
    learn_rate = 0.01
    epochs = 100

    return {
        'weights_1': weights_1,
        'bias_1': bias_1,
        'weights_2': weights_2,
        'bias_2': bias_2,
        'learn_rate': learn_rate,
        'epochs': epochs
    }
neural_network_params = initialize_neural_network()

#3
def softMax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def softMax_derivative(x):
    return softMax(x) * (1 - softMax(x))

def error(output, target):
    return output - target

#4+5
def back_propagation(seed, neural_network_params, learn_rate=0.01):
    # Unpack neural network parameters
    weights_1 = neural_network_params.get('weights_1')
    bias_1 = neural_network_params.get('bias_1')
    weights_2 = neural_network_params.get('weights_2')
    bias_2 = neural_network_params.get('bias_2')

    # Forward propagation
    hidden_pre = bias_1 + weights_1.dot(seed)
    hidden = softMax(hidden_pre)

    output_pre = bias_2 + weights_2.dot(hidden)
    output = softMax(output_pre)

    # Compute error
    error = output - lbl

    # Backward propagation
    gradient = error * softMax_derivative(output_pre)
    weights_2 -= learn_rate * gradient.dot(np.transpose(hidden))
    bias_2 -= learn_rate * gradient

    gradient = np.transpose(weights_2).dot(gradient) * softMax_derivative(hidden_pre)
    weights_1 -= learn_rate * gradient.dot(np.transpose(seed))
    bias_1 -= learn_rate * gradient

#6
epochs = neural_network_params.get('epochs')
for epoch in range(epochs):
    # Iterate over training samples
    for seed, lbl in zip(train_features, train_labels):
        seed.shape += (1,)
        lbl.shape += (1,)
        back_propagation(seed, neural_network_params)
    if epoch % 5 == 0:
        print('Epoch: ', epoch)

correct_cases = 0
for seed, lbl in zip(test_features, test_labels):
    seed.shape += (1,)
    lbl.shape += (1,)
    hidden_pre = neural_network_params.get('bias_1') + neural_network_params.get('weights_1').dot(seed)
    hidden = softMax(hidden_pre)
    output_pre = neural_network_params.get('bias_2') + neural_network_params.get('weights_2').dot(hidden)
    output = softMax(output_pre)
    if np.argmax(output) == np.argmax(lbl):
        correct_cases += 1
#print in percent, with no decimals, the accuracy of the model on the test set
print('Accuracy: ', round((correct_cases / test_features.shape[0]) * 100, 2), '%')
