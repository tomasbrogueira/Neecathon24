import cv2
import numpy as np
from tensorflow import keras

# Load the pre-trained model
model = keras.models.load_model("model_10_epochs.h5")

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize the webcam
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit if frame not read properly

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    status = "No Face Detected"

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        status = "Face Detected"
        for (x, y, w, h) in faces:
            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            face_roi_gray = gray[y:y + h, x:x + w]
            face_roi_color = frame[y:y + h, x:x + w]

            # Detect eyes within the face region
            eyes = eye_cascade.detectMultiScale(face_roi_gray)
            if len(eyes) > 0:
                for (ex, ey, ew, eh) in eyes:

                    eyes_roi = face_roi_color[ey:ey + eh, ex:ex + ew]

                    # Preprocess the eye image for prediction
                    final_image = cv2.resize(eyes_roi, (224, 224))
                    final_image = np.expand_dims(final_image, axis=0)
                    final_image = final_image / 255.0

                    # Make prediction
                    predictions = model.predict(final_image)
                    if predictions[0][0] > 0.5:
                        status = "Awake"
                    else:
                        status = "Drowsy"
                    break  # Process only the first detected eye
            else:
                status = "Eyes Not Detected"
                print("Eyes are not detected")
            break  # Process only the first detected face
    else:
        status = "No Face Detected"

    # Display the status on the frame
    cv2.putText(frame, status, (50, 50), font, 1, (0, 0, 255), 2, cv2.LINE_4)
    cv2.imshow('Drowsiness Detection', frame)

    # Exit condition
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
