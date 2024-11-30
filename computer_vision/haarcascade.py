import cv2
import matplotlib.pyplot as plt 
import numpy as np

# Read random image from dataset
img = cv2.imread('dataset/Closed_Eyes/s0001_00002_0_0_0_0_0_01.png')

# Check if the image was loaded successfully
if img is None:
    raise ValueError("Image not found or the path is incorrect.")

# Initialize the Haar cascades for face and eye detection
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect eyes in the image
eyes = eyeCascade.detectMultiScale(gray, 1.1, 4)

# Draw rectangles around detected eyes
for (x, y, w, h) in eyes:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Convert the image from BGR to RGB for displaying with matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


# crop eye image

eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
for (x, y, w, h) in eyes:
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    eyes = eye_cascade.detectMultiScale(roi_gray)
    if len(eyes) == 0:
        print("eyes are not detected")
    else:
        for (ex, ey, ew, eh) in eyes:
            eyes_roi = roi_color[ey: ey + eh, ex: ex + ew]



final_image = cv2.resize(eyes_roi, (224, 224))
final_image = np.expand_dims(final_image, axis = 0) ## need fourth dimension
final_image = final_image/225.0


from tensorflow import keras
from tensorflow.keras import layers
model = keras.models.load_model("pre_trained_model.h5")


print(model.predict(final_image))


# Display the image
plt.imshow(cv2.cvtColor(eyes_roi, cv2.COLOR_BGR2RGB))  # Display the image
plt.axis('off')  # Optional: Hide axis
plt.title('Detected Eyes')  # Optional: Add a title
plt.show()  # This line displays the plot
