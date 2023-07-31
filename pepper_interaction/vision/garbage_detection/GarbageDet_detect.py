import subprocess
import os
import socket
import threading

def detect(img_path):
    ris = subprocess.run(["python", os.getcwd()+"/yolov5/detect.py", "--weights", "model/best.pt", "--img", "640", "--conf", "0.05", "--source", str(img_path)], capture_output=True, text=True) # add "--half" if you have GPUs!
    print(ris.stderr)
    return ris.stdout

def handle_client(client_socket, client_address):
    try:
        print("Connected to:", client_address)
        while True:
            # receive data from the client --> (obj_class and 'fullness' of the bins)
            img_path = client_socket.recv(1024).decode('utf-8')
            if not img_path:
                break
            print("Received:", img_path)
            ris = detect(img_path) # modified data is a string in the format "ris_class,ris_img_path"
            # send the modified data back to the client
            client_socket.sendall(ris.encode("utf-8"))     
    except Exception as e:
        print("Error:", e)   
    finally:
        client_socket.close()
        print("Connection closed with:", client_address)

if __name__ == "__main__":
    # create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a specific address and port
    server_address = ('127.0.0.1', 3030)
    server_socket.bind(server_address)
    # listen for incoming connections (max 1 pending connection)
    server_socket.listen(5)
    print("Waiting for a connection...") 
    try:
        while True:
            # accept a connection
            client_socket, client_address = server_socket.accept()
            # start a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        # clean up the server socket
        server_socket.close()
