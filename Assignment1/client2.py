import threading
import socket
import json
import time
import os

# Define constants
HEADER = 64 
FORMAT = "utf-8"
CENTRAL_SERVER_IP = socket.gethostbyname(socket.gethostname())
CENTRAL_SERVER_PORT = 5050  # Adjust the port as needed
hostname = socket.gethostname()
file_path = r"C:\Users\Admin\OneDrive\Documents\BKU\Junior\Computer Networking"
output_folder = r"C:\Users\Admin\OneDrive\Documents\BKU\Junior\Computer Networking"

class PeerClient(threading.Thread):
    def __init__(self, name, ip, port,file):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port = port
        self.conn = None
        self.running = True
        self.file = file
        # self.hello_printed = threading.Event()

    def run(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((self.ip, self.port))
        except Exception as e:
            print(f"Error connecting to {self.name}: {e}")
            return

        # Now, you can send and receive messages through self.conn
        while self.running:
            try:
                filename = 'drazod.txt'
                outfile_path = os.path.join(output_folder, filename)
                self.send_message(self.file)
                data = b''
                f = open(outfile_path, 'wb')
                self.conn.settimeout(5)
                while True:
                    try:
                        m = self.conn.recv(1024)
                        if not m:
                            break  # No more data to read, the connection is closed
                        data += m  # Accumulate the received data
                    except socket.timeout:
                        print("Receive timeout. No more data.")
                        break
                f.write(data)
                f.close()             
                # print(f"Received from {self.name}: {data.decode(FORMAT)}")
                self.close_connection()
            except Exception as e:
                print(f"Error while receiving from {self.name}: {e}")
                break

    def send_message(self, message):
        if self.conn:
            self.conn.send(message.encode())
        else:
            print("Connection not established.")

    def close_connection(self):
        if self.conn:
            self.conn.close()
        self.running = False

def reponse():
    while True:
            msg_length = central_server_socket.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                message = central_server_socket.recv(msg_length).decode(FORMAT)
                print("Server says:", message)
                try: 
                    ip,port = message.split()
                    command = user_input.split()
                    # ip = "192.168.8.156"#input("Please enter the IP you receive:")
                    peer_client = PeerClient("YourPeerName",ip,port,command[1])
                    peer_client.start()
                    peer_client.join()
                except:
                    print("No peer need")
            if not message:
                break  # Connection closed
                # Handle received data from the central server
    

def publish(msg):
    try:
        cmd_lenght = len(msg)
        send_length = str(cmd_lenght).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        central_server_socket.send(send_length)
        central_server_socket.send(msg.encode(FORMAT))  # Send peer's name to the central server
        # Now, you can send and receive messages from the central server
    except Exception as e:
        print(f"Error communicating with the central server: {e}")

def fetch(msg):
    try:
        cmd_lenght = len(msg)
        send_length = str(cmd_lenght).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        central_server_socket.send(send_length)
        central_server_socket.send(msg.encode(FORMAT))  # Send peer's name to the central server
        # Now, you can send and receive messages from the central server
    except Exception as e:
        print(f"Error communicating with the central server: {e}")

def P2P():
    # Input your local IP and port (your address)
    local_ip = socket.gethostbyname(hostname)
    local_port = 69

    # Specify your peer's name
    peer_name = "YourPeerName"

    # Create a server socket to accept incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_ip, local_port))
    server_socket.listen(5)  # Listen for incoming connections

    print(f"Server is listening on {local_ip}:{local_port}")

    # Start a thread to communicate with the central server

    peer_clients = []

    while True:
            # Accept incoming connections
            conn, addr = server_socket.accept()
            print(f'{addr} connected')
            message = conn.recv(1024).decode(FORMAT)
            filename = message
            openfile_path = os.path.join(file_path, filename)
            try:
                f = open(openfile_path, 'rb') 
                l = os.path.getsize(file_path)
                m = f.read(l)
                conn.sendall(m)
                f.close()
            except:
                continue
            # server_socket.send(addr.encode(FORMAT))


central_server_thread = threading.Thread(target=P2P)
central_server_thread.daemon = True
central_server_thread.start()

central_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
central_server_socket.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))
central_server_response_thread = threading.Thread(target=reponse)
central_server_response_thread.daemon = True
central_server_response_thread.start()

if __name__ == "__main__":
    while True:
        time.sleep(1)
        user_input = input("Enter your command: ")
        if user_input.startswith('publish'):
            publish(user_input)
        elif user_input.startswith('fetch'):
            fetch(user_input)
