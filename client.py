import socket
import cv2
import pickle
import struct

#providing server ip and port
IP = "127.0.0.1"
family = socket.AF_INET
protocol = socket.SOCK_STREAM
clien = socket.socket(family, protocol)
clien.connect((IP, 7777))

def video_stream(client):
    data = b""
    payload_size = struct.calcsize("Q")
    # Add your video streaming logic here
    while True:
        while len(data) < payload_size:
            packet = clien.recv(4096)
            
            if not packet: 
                break
            data+=packet
        packed_msg = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg)[0]
        
        while len(data) < msg_size:
            data += clien.recv(4096)
        frame = data[:msg_size]
        data  = data[msg_size:]
        vid = pickle.loads(frame)
        cv2.imshow("Video from Client",vid)
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
            break

# New function for chat
def chat_with_server(clien):
    while True:
        message = input("You: ")
        clien.send(message.encode())
        if message.lower() == "exit":
            break
        server_response = clien.recv(1024).decode()
        print("Server:", server_response)

# New function for file transfer
def receive_file_from_server(clien, file_name):
    file_data = clien.recv(4096)
    with open(file_name, "wb") as file:
        file.write(file_data)
    print(f"File {file_name} received from the server.")

print("Enter 1 for video streaming, 2 for chat, 3 for file transfer:")
choice = input()
clien.send(choice.encode())

if choice == "1":
    print("Video streaming mode enabled.")
    video_stream(clien)
elif choice == "2":
    print("Chat mode enabled with the server.")
    chat_with_server(clien)
elif choice == "3":
    file_name = input("Enter the file name to request from the server: ")
    clien.send(file_name.encode())
    receive_file_from_server(clien, file_name)

clien.close()
