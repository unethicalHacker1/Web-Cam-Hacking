import socket
import cv2
import numpy as np
import pickle
import struct

# Server settings
HOST = '127.0.0.1'  # Change this to your actual IP if needed
PORT = 9999         # Server port

# Set up a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server listening on {HOST}:{PORT}")

# Accept a connection from the client
client_socket, addr = server_socket.accept()
print(f"Connection established with {addr}")

# Prepare to receive video data
data = b""
payload_size = struct.calcsize("L")

# Initialize the VideoWriter to save the video
# Assuming default resolution, modify if needed based on client resolution
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_from_client.mp4', fourcc, 20.0, (640, 480))

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4096)
        if not packet:  # Connection closed by client
            break
        data += packet

    if not packet:
        break

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Deserialize and decode the frame
    try:
        buffer = pickle.loads(frame_data)
        frame = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Failed to decode frame: {e}")
        continue

    if frame is None:
        print("Failed to decode frame")
        continue

    # Display the frame on the server side and write to video file
    cv2.imshow('Server - Receiving Video', frame)
    out.write(frame)

    # Add print statement to confirm frame capture
    print("Frame captured and processed")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video writer and close all windows
out.release()
cv2.destroyAllWindows()
client_socket.close()
server_socket.close()