import cv2
import numpy as np
from tensorflow import keras
import socket
import struct
import pickle
from collections import deque

# ==================== Hyperparameters ====================
WINDOW_SIZE = 20           # Number of recent frames to consider
DROWSY_RATIO_THRESHOLD = 0.8  # Ratio of "Drowsy" frames to trigger alert
# =========================================================

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

# Initialize deque to store the status of the latest WINDOW_SIZE frames
status_queue = deque(maxlen=WINDOW_SIZE)

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
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 178, 102), 2)

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
                            current_status = "Awake"
                        else:
                            current_status = "Drowsy"
                        status = current_status
                        break  # Process only the first detected eye
                else:
                    current_status = "Eyes Not Detected"
                    status = current_status
                    print("Eyes are not detected")
                break  # Process only the first detected face
        else:
            current_status = "No Face Detected"
            status = current_status

        # Append the current status to the queue
        status_queue.append(current_status)

        # Calculate the ratio of "Drowsy" frames in the queue
        if len(status_queue) == WINDOW_SIZE:
            drowsy_count = sum(1 for s in status_queue if s == "Drowsy")
            drowsy_ratio = drowsy_count / WINDOW_SIZE
        else:
            drowsy_ratio = 0  # Not enough data yet

        # Determine overall status based on the drowsy_ratio
        if drowsy_ratio >= DROWSY_RATIO_THRESHOLD:
            overall_status = "ALERT! Person is Sleeping"
            color = (0, 0, 255)  # Red
        elif status == "Drowsy":
            overall_status = "Drowsy"
            color = (0, 255, 255)  # Yellow
        else:
            overall_status = status
            color = (0, 255, 0)  # Green

        # Display the status on the frame
        cv2.putText(frame, overall_status, (50, 50), font, 1, color, 2, cv2.LINE_AA)

        # Optionally, display the drowsy ratio
        ratio_text = f"Drowsy Ratio: {drowsy_ratio:.2f}"
        cv2.putText(frame, ratio_text, (50, 90), font, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow('Drowsiness Detection', frame)

        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
