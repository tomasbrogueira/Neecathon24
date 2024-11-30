import cv2
import socket
import struct
import pickle

# Configurar socket
HOST = '0.0.0.0'  # Use localhost
PORT = 9999 # Porta para comunicação
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Aguardando conexão...")
conn, addr = server_socket.accept()
print(f"Conectado por: {addr}")

data = b""
payload_size = struct.calcsize(">L")

try:
    while True:
        # Receber tamanho do frame
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_size = data[:payload_size]
        data = data[payload_size:]
        frame_size = struct.unpack(">L", packed_size)[0]
        
        # Receber frame completo
        while len(data) < frame_size:
            data += conn.recv(4096)
        frame_data = data[:frame_size]
        data = data[frame_size:]
        
        # Desserializar o frame
        frame = pickle.loads(frame_data)
        
        # Mostrar o frame recebido
        cv2.imshow('Recebendo Vídeo', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    conn.close()
    server_socket.close()
