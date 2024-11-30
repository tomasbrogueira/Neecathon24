import os
import cv2
import matplotlib.pyplot as plt

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
