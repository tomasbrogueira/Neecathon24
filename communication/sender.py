import cv2
import socket
import struct
import pickle

# Configurar socket
HOST = '172.20.199.123'  # Use localhost do programa em si
PORT = 9999 # Porta para comunicação
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
connection = client_socket.makefile('wb')

# Inicializar câmara
cap = cv2.VideoCapture(0)  # Usa a câmara do PC

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Serializar o frame
        data = pickle.dumps(frame)
        size = len(data)
        
        # Enviar o tamanho do frame e os dados
        client_socket.sendall(struct.pack(">L", size) + data)

finally:
    cap.release()
    client_socket.close()
