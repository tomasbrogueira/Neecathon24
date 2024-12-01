import cv2
import numpy as np
from tensorflow import keras
import socket
import struct
import pickle
from collections import deque

# Hyperparameters
WINDOW_SIZE = 20
DROWSY_RATIO_THRESHOLD = 0.8

# Initialize deque to store the status of the latest WINDOW_SIZE frames
status_queue = deque(maxlen=WINDOW_SIZE)

# ML model and cascades
model = keras.models.load_model("model_10_epochs.h5")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Socket setup
HOST = '0.0.0.0'
PORT = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Waiting for connection...")
conn, addr = server_socket.accept()

data = b""
payload_size = struct.calcsize(">L")


try:
    with open("drowsy_ratio.txt", "w") as f:
        while True:
            # Video frame processing (same as before)
            while len(data) < payload_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            if len(data) < payload_size:
                break

            packed_size = data[:payload_size]
            data = data[payload_size:]
            frame_size = struct.unpack(">L", packed_size)[0]

            while len(data) < frame_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            if len(data) < frame_size:
                break

            frame_data = data[:frame_size]
            data = data[frame_size:]

            frame = pickle.loads(frame_data)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            status = "No Face Detected"

            if len(faces) > 0:
                status = "Face Detected"
                for (x, y, w, h) in faces:
                    face_roi_gray = gray[y:y + h, x:x + w]
                    eyes = eye_cascade.detectMultiScale(face_roi_gray)
                    if len(eyes) > 0:
                        for (ex, ey, ew, eh) in eyes:
                            eyes_roi = face_roi_gray[ey:ey + eh, ex:ex + ew]
                            final_image = cv2.resize(eyes_roi, (224, 224))
                            final_image = np.expand_dims(final_image, axis=0)
                            final_image = final_image / 255.0

                            predictions = model.predict(final_image)
                            status = "Awake" if predictions[0][0] > 0.5 else "Drowsy"
                            break

            status_queue.append(status)
            drowsy_count = sum(1 for s in status_queue if s == "Drowsy")
            drowsy_ratio = drowsy_count / len(status_queue) if status_queue else 0

            # Write the drowsy ratio to a file
            f.write(f"{drowsy_ratio}\n")

finally:
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
