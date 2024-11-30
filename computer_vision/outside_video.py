import cv2
import numpy as np
from tensorflow import keras
import socket
import struct
import pickle

# Load the pre-trained model
model = keras.models.load_model("model_10_epochs.h5")

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Configure socket to receive video frames
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 9999       # Port to listen on
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Waiting for connection...")
conn, addr = server_socket.accept()
print(f"Connected by: {addr}")

data = b""
payload_size = struct.calcsize(">L")

font = cv2.FONT_HERSHEY_SIMPLEX

try:
    while True:
        # Receive message size
        while len(data) < payload_size:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        if len(data) < payload_size:
            break  # Incomplete packet, exit loop

        packed_size = data[:payload_size]
        data = data[payload_size:]
        frame_size = struct.unpack(">L", packed_size)[0]

        # Receive frame data
        while len(data) < frame_size:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        if len(data) < frame_size:
            break  # Incomplete frame, exit loop

        frame_data = data[:frame_size]
        data = data[frame_size:]

        # Deserialize frame
        frame = pickle.loads(frame_data)

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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
