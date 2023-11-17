'''
               __
              / _)
     _/\/\/\_/ /
   _|         /
 _|  (  | (  |
/__.-'|_|--|_|  PapaJ
'''
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
SUCCESS_MESSAGE = "Kết nối thành công - 1"
hostname = socket.gethostname()
file_path = None
output_folder = None
local_ip = socket.gethostbyname(hostname)
local_port = 81
flag = True
configg = {}
# Load the configuration




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
                filename = str(self.file)
                outfile_path = os.path.join(file_path, filename)
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
                self.conn.settimeout(10)
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
def config():
    global file_path
    global output_folder
    config_file_path = r"C:\Users\Admin\OneDrive\Documents\BKU\Junior\ComputerNetworking\P2P\Assignment1\drazod\config.json"
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)

    # Access configuration values
    file_path = config["file_path"]
    output_folder = config["output_folder"]

def save_config():
    # Save the updated configuration to the file
    with open(config_file_path, 'w') as config_file:
        json.dump(configg, config_file, indent=4)
#=======================================================================================================
#NEW
def send_to_server(client,message):
    notify = message.encode(FORMAT)
    notify_lenght = len(notify)
    send_length = str(notify_lenght).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(notify)

#MORE NEW
def register_user(username, password, confirm):
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


    send_to_server(central_server_socket, 'register')
    send_to_server(central_server_socket, username)
    send_to_server(central_server_socket, password)
    send_to_server(central_server_socket, str(local_port))
#NEW
def login_user(username, password):

    send_to_server(central_server_socket, 'login')
    send_to_server(central_server_socket, username)
    send_to_server(central_server_socket, password)
    send_to_server(central_server_socket,str(local_port))
    time.sleep(2)
    return flag

def logout_user():
    send_to_server(central_server_socket, 'logout')
    time.sleep(2)
    exit()

#=======================================================================================================

def reponse():
    global flag
    config()
    while True:
            msg_length = central_server_socket.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                message = central_server_socket.recv(msg_length).decode(FORMAT)
                print("Server says:", message)
                if message == SUCCESS_MESSAGE:
                    flag = False
                else:
                    try: 
                        ip,port,fname = message.split()
                        # command = user_input.split()
                        peer_client = PeerClient(1,ip,int(port),fname)
                        peer_client.start()
                        peer_client.join()
                    except:
                        continue
            if not message:
                break  # Connection closed
                # Handle received data from the central server
    

def publish(msg):
    config()
    localname = msg.split()[1]
    filename = msg.split()[2]
    try:
    #Make respitory
        repository_path = file_path 
        os.makedirs(repository_path, exist_ok=True)

        # Move the file to the repository
        source_path = os.path.join(output_folder, filename)
        target_path = os.path.join(repository_path, filename)  
        os.rename(source_path,target_path)
    except:
        print("Invalid Filename path or File name had been added to repository")

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
    config()
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
                        config()
                        repository_path = file_path  # Replace with the actual repository path
                        files_in_repository = os.listdir(repository_path)

        # Create a string containing the file names, separated by spaces
                        data = " ".join(files_in_repository)
                        data_lenght = len(data)
                        send_length = str(data_lenght).encode(FORMAT)
                        send_length += b' ' * (HEADER - len(send_length))
                        conn.send(send_length)
                        conn.send(data.encode(FORMAT)) 
#-----------------------------------------------P2P FILE TRANSFER---------------------------------------------------------#
                    else:  
                        config()
                        filename = message
                        openfile_path = os.path.join(file_path, filename)
                        with open(openfile_path, 'rb') as f:
                            while True:
                                data = f.read(1024)  # Read 1KB at a time
                                if not data:
                                    break
                                conn.send(data)
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
    while flag:
        user_input = input("Enter your command (login/register): ").lower()
        if user_input == "login":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_user(username, password)
        elif user_input == "register":
            username = input("Enter username: ")
            password = input("Enter password: ")
            confirm = input("Confirm password: ")
            register_user(username, password, confirm)
        time.sleep(2)

    file_path = input("Choose Path you want to make your Repository:")
    config_file_path = r"C:\Users\Admin\OneDrive\Documents\BKU\Junior\ComputerNetworking\P2P\Assignment1\drazod\config.json"  # Adjust the path to your configuration file
    with open(config_file_path, 'r') as config_file:
        configg = json.load(config_file)
        configg["file_path"] = file_path
        save_config()
#------------------------------------------------------------//-----------------------------------------------------------#
    while True:
        user_input = input("Enter your command: ")
        if user_input.startswith('publish'):
            output_folder = input("Choose Path you want to publish file:")
            with open(config_file_path, 'r') as config_file:
                configg = json.load(config_file)
                configg["output_folder"] = output_folder
                save_config()
            publish(user_input)
        elif user_input.startswith('fetch'):
            fetch(user_input)
        else:
            logout_user()
        time.sleep(2)

