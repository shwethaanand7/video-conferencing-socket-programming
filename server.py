import socket
import cv2
import pickle
import struct

print("MIT License\nCopyright© Divya & Shwetha 2023")

# Socket Create
IP = "127.0.0.1"
family = socket.AF_INET
protocol = socket.SOCK_STREAM
serv = socket.socket(family, protocol)

# binding IP address with the port
serv.bind((IP, 7777))
serv.listen(5)

# New function for video streaming
def video_stream_to_client(clien):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        img, frame = cap.read()
        a = pickle.dumps(frame)
        message = struct.pack("Q", len(a)) + a
        clien.sendall(message)
        cv2.imshow('Video from Server', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

# New function for chat
def chat_with_client(clien):
    while True:
        message = clien.recv(1024).decode()
        print("Client:", message)
        response = input("You: ")
        clien.send(response.encode())
        if response.lower() == "exit":
            break

# New function for file transfer
def file_transfer_with_client(clien):
    file_name = clien.recv(1024).decode()
    try:
        with open(file_name, "rb") as file:
            file_data = file.read()
        clien.send(file_data)
        print(f"File {file_name} sent to the client.")
    except FileNotFoundError:
        print(f"File {file_name} not found.")

while True:
    clien, addr = serv.accept()
    if clien:
        print("Client connected:", addr)
        choice = clien.recv(1).decode()

        if choice == "1":
            print("Video streaming mode enabled with the client.")
            # video_thread = threading.Thread(target=video_stream_to_client, args=(clien,))
            # video_thread.daemon = True
            # video_thread.start()
            video_stream_to_client(clien)
        elif choice == "2":
            print("Chat mode enabled with the client.")
            chat_with_client(clien)
        elif choice == "3":
            print("File transfer mode enabled with the client.")
            file_transfer_with_client(clien)
        
        clien.close()
