import csv
import numpy as np
import tensorflow as tf

csvFile = open("", "r")
reader = csv.reader(csvFile)
data = list(reader)  # Reading the configured data

data = np.array(data)  # Convert the data into numpy format
data = data.T  # Transpose the data to be vertical

labels = data[0]  # Record the data labels
train = data[1:5]  # Record the training data

train = np.array(train).T  # Transpose the training data back into original format

labels = tf.keras.utils.to_categorical(labels, num_classes=2)  # Define labels with tensorflow

model = tf.keras.Sequential([  # Configure layout of the neural network
    tf.keras.layers.Input(shape=(300,)),
    tf.keras.layers.Dense(768, activation='relu'),
    tf.keras.layers.Dense(768, activation='relu'),
    tf.keras.layers.Dense(768, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])
