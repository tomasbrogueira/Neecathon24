# using transfer learning to train a model to detect drowsiness

import tensorflow as tf ## pip install tensorflow-gpu 
import cv2  ## pip install opencv-python
## pip install opencv-contrib-python     fullpackage
import os
import matplotlib.pyplot as plt ## pip install matplotlib
import numpy as np ## pip install numpy


Datadirectory = "dataset/" ## folder where the dataset is stored
Classes = ["Closed_Eyes", "Open_Eyes"] ## classes of the dataset
for category in Classes:
    # difference
    path = os.path.join(Datadirectory, category)
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
        backtorgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        plt.imshow(img_array, cmap='gray')
        plt.show()
        break
    break



