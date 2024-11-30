# using transfer learning to train a model to detect drowsiness

# pip install pyyaml h5py  # Required to save models in HDF5 format



import tensorflow as tf ## pip install tensorflow-gpu 
import cv2  ## pip install opencv-python
## pip install opencv-contrib-python     fullpackage
import os
import matplotlib.pyplot as plt ## pip install matplotlib
import numpy as np ## pip install numpy
import random as rn

from computer_vision.building_files.preprocessing import create_data


Datadirectory = "dataset/" ## folder where the dataset is stored
Classes = ["Closed_Eyes", "Open_Eyes"] ## classes of the dataset
Image_size = 224


data = create_data(Classes, Datadirectory, Image_size)

# shuffle the data
rn.shuffle(data)


# working with training data   - Y difference
X = []
Y = []

for features, label in data:
    X.append(features)
    Y.append(label)

X = np.array(X).reshape(-1, Image_size, Image_size, 3)


# normalize the data
X = X/255.0

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Assuming X and Y are already defined and preprocessed
Y = np.array(Y)

print(X.shape, Y.shape)

# Load the model
model = keras.applications.mobilenet.MobileNet() # rgb images 224x224
model.summary()

# Transfer learning
base_input = model.input  # Correctly get the input layer
base_output = model.layers[-4].output
Flat_layer = layers.Flatten()(base_output)
final_output = layers.Dense(1)(Flat_layer)  # 1 because we have 2 classes
final_output = layers.Activation('sigmoid')(final_output)

custom_model = keras.Model(inputs=base_input, outputs=final_output)

custom_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
custom_model.fit(X, Y, epochs=10, validation_split=0.1)

# Save the model
custom_model.save("model.h5")

# Load the model
# model = keras.models.load_model("model.h5")

