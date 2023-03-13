import random
import pandas as pd
from math import exp
from sklearn.preprocessing import OneHotEncoder

input_size = hidden_neurons = output_neurons = learning_rate = epochs = 0
weights_input_hidden = weights_hidden_output = tetras = list()

dataset = pd.DataFrame(columns=['X1', 'X2', 'X3', 'X4', 'Y'])
test_dataset = pd.DataFrame(columns=['X1', 'X2', 'X3', 'X4', 'Y'])


def initialize() -> None:
    global dataset, test_dataset

    for line in open('iris.data', 'r').read().split('\n'):
        splitted_line = line.split(',')
        if random.choice([1, 2, 3, 4, 5]) == 1:
            test_dataset.loc[len(test_dataset)] = splitted_line
        else:
            dataset.loc[len(dataset)] = splitted_line

    dataset = encode(dataset)
    test_dataset = encode(test_dataset)

    # print(dataset)
    # print(test_dataset)


def encode(data: pd.DataFrame) -> pd.DataFrame:
    cat_features = data[['Y']]
    enc = OneHotEncoder(sparse=False).fit(cat_features)
    encoded = pd.DataFrame(enc.transform(cat_features),
                           columns=enc.categories_[0])
    data = pd.concat([data, encoded], axis=1).drop(columns=['Y'])

    return data


def param_initialize() -> None:
    global input_size, hidden_neurons, output_neurons, learning_rate, epochs
    global weights_input_hidden, weights_hidden_output, tetras
    input_size = 4
    hidden_neurons = 4
    output_neurons = 3

    weights_input_hidden = [random.uniform(-0.5, 0.5) for i in range(input_size * hidden_neurons)]
    weights_hidden_output = [random.uniform(-0.5, 0.5) for i in range(hidden_neurons * output_neurons)]
    tetras = [random.uniform(0, 1) for i in range(input_size + hidden_neurons + output_neurons)]


def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))


def derivative(x: float) -> float:
    return x * (1 - x)


def check_error(expected: list, real: list) -> float:
    return sum(abs(expected[index] - real[index]) for index in range(len(expected)))


def forward_propagation(input_line: pd.Series) -> None:
    hidden_outputs = list()
    expected = [input_line['Iris-setosa'], input_line['Iris-versicolor'], input_line['Iris-virginica']]

    for hidden_neuron_index in range(hidden_neurons):
        output = 0
        for weights_index in range(hidden_neuron_index * input_size, (hidden_neuron_index + 1) * input_size):
            output += weights_input_hidden[weights_index] * float(input_line[weights_index % input_size])
        hidden_outputs.append(sigmoid(output - tetras[hidden_neuron_index]))

    outputs = list()
    for output_neuron_index in range(output_neurons):
        neuron_output = 0
        for hidden_neuron_index in range(output_neuron_index * hidden_neurons, (output_neuron_index + 1) * hidden_neurons):
            neuron_output += weights_hidden_output[hidden_neuron_index] * hidden_outputs[hidden_neuron_index % hidden_neurons]
        outputs.append(sigmoid(neuron_output - tetras[len(tetras) - 1 - output_neuron_index]))

    print(f"Computed: {outputs}")
    print(f"Expected: {expected}")
    print(f"Error: {check_error(expected, outputs)}")


if __name__ == '__main__':
    initialize()
    param_initialize()

    forward_propagation(dataset.loc[0])
