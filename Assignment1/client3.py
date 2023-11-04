import threading
import socket
import json
import time
import os
import re #NEW

# Define constants
HEADER = 64 
FORMAT = "utf-8"
CENTRAL_SERVER_IP = socket.gethostbyname(socket.gethostname())
CENTRAL_SERVER_PORT = 5050  # Adjust the port as needed
hostname = socket.gethostname()
file_path = None
output_folder = None

published_files = []

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
#------------------------------------------Path---------------------------------------------------------------------------#                
                filename = 'drazod.txt'
                outfile_path = os.path.join(output_folder, filename)
#------------------------------------------Send Request-------------------------------------------------------------------#
                msg = str(self.file)
                cmd_lenght = len(msg)
                send_length = str(cmd_lenght).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                self.conn.send(send_length)
                self.conn.send(msg.encode(FORMAT))
#-------------------------------------------Receive-----------------------------------------------------------------------#
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

#=======================================================================================================
#NEW
def sendMessage(client,message):
    notify = message.encode(FORMAT)
    notify_lenght = len(notify)
    send_length = str(notify_lenght).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(notify)
    
#MORE NEW
def register_user(username, password, confirm, user_id, port):
    if not re.match("^[a-zA-Z][a-zA-Z0-9]{3,11}$", username):
        print("Error: Invalid username!")
        return
#Password must contain at least: 8 normal character long, 1 upeercase, 1 special character
    if not re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
        print("Error: Invalid password!")
        return

    if password != confirm:
        print("Error: Password confirmation does not match!")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))

    send_to_server(client_socket, json.dumps({"action": "register", "username": username}))
    send_to_server(client_socket, json.dumps({"password": password}))
    send_to_server(client_socket, json.dumps({"id": user_id}))
    send_to_server(client_socket, json.dumps({"port": port}))

    client_socket.close()
#NEW
def login_user(username, password):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))

    send_to_server(client_socket, json.dumps({"action": "register", "username": username}))
    send_to_server(client_socket, json.dumps({"password": password}))

#=======================================================================================================

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
                    peer_client = PeerClient(1,ip,int(port),command[1])
                    peer_client.start()
                    peer_client.join()
                except:
                    continue
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

        published_files.append(msg.split()[2])
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
#-------------------------------------------------------CLient Server side socket-----------------------------------------#
    local_ip = socket.gethostbyname(hostname)
    local_port = 71

    # Specify your peer's name
    peer_name = "YourPeerName"

    # Create a server socket to accept incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_ip, local_port))
    server_socket.listen(5)  # Listen for incoming connections

    print(f"Server is listening on {local_ip}:{local_port}")

    # Start a thread to communicate with the central server

    while True:
            # Accept incoming connections
            conn, addr = server_socket.accept()
            print(f'{addr} connected')
            try:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int (msg_length)
                    message = conn.recv(msg_length).decode(FORMAT)
                    if message == 'discover':
                        data = " ".join(['publish', ' '.join(published_files)])
                        data_lenght = len(data)
                        send_length = str(data_lenght).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(data.encode(FORMAT)) 
#-----------------------------------------------P2P FILE TRANSFER---------------------------------------------------------#
                    else:  
                        filename = message
                        openfile_path = os.path.join(file_path, filename)
                        f = open(openfile_path, 'rb') 
                        l = os.path.getsize(file_path)
                        m = f.read(l)
                        conn.sendall(m)
                        f.close()
            except:
                continue
#-------------------------------------------------------------------------------------------------------------------------#


central_server_thread = threading.Thread(target=P2P)
central_server_thread.daemon = True
central_server_thread.start()

central_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
central_server_socket.connect((CENTRAL_SERVER_IP, CENTRAL_SERVER_PORT))
central_server_response_thread = threading.Thread(target=reponse)
central_server_response_thread.daemon = True
central_server_response_thread.start()

if __name__ == "__main__":
#--------------------------------------------------------Login Phase------------------------------------------------------#
    user_input = input("Enter your command (login/register): ").lower()
    if user_input == "login":
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_user(username, password)
    elif user_input == "register":
        username = input("Enter username: ")
        password = input("Enter password: ")
        confirm = input("Confirm password: ")
        user_id = input("Enter ID: ")
        port = input("Enter port: ")
        register_user(username, password, confirm, user_id, port)
    file_path = input("Enter your path to folder you want to send file:")
    output_folder = input("Enter your path to folder you want to get file:")
#------------------------------------------------------------//-----------------------------------------------------------#
    while True:
        time.sleep(1)
        user_input = input("Enter your command: ")
        if user_input.startswith('publish'):
            publish(user_input)
        elif user_input.startswith('fetch'):
            fetch(user_input)
