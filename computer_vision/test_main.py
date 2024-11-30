import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from computer_vision.main import create_data

# FILE: computer_vision/test_main.py


def test_model_compilation():
    # Create mock data
    X = np.random.rand(10, 224, 224, 3)
    Y = np.random.randint(2, size=(10,))

    # Load the model
    model = keras.applications.mobilenet.MobileNet()
    base_input = model.input
    base_output = model.layers[-4].output
    final_output = layers.Dense(1)(base_output)
    final_output = layers.Activation('sigmoid')(final_output)
    custom_model = keras.Model(inputs=base_input, outputs=final_output)

    # Compile the model
    custom_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    # Check if the model is compiled
    assert custom_model.optimizer is not None

def test_model_training():
    # Create mock data
    X = np.random.rand(10, 224, 224, 3)
    Y = np.random.randint(2, size=(10,))

    # Load the model
    model = keras.applications.mobilenet.MobileNet()
    base_input = model.input
    base_output = model.layers[-4].output
    final_output = layers.Dense(1)(base_output)
    final_output = layers.Activation('sigmoid')(final_output)
    custom_model = keras.Model(inputs=base_input, outputs=final_output)

    # Compile the model
    custom_model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    # Train the model
    history = custom_model.fit(X, Y, epochs=1, validation_split=0.1)

    # Check if the model trained without errors
    assert history is not None