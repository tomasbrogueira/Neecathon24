import os
import cv2

def create_data(CLASSES, DATADIR, IMG_SIZE):
    data = []
    for category in CLASSES:
        path = os.path.join(DATADIR, category) # path to the dataset
        class_num = CLASSES.index(category) # get the classification  (0 or a 1). 0=CLOSED, 1=OPEN
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                backtorgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
                new_array = cv2.resize(backtorgb, (IMG_SIZE, IMG_SIZE))
                data.append([new_array, class_num])
            except Exception as e:
                pass
    return data

