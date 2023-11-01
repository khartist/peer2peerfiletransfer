import socket
import pickle
'''
def share_files():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 9090))
    s.listen(5)
    print("Listening for file requests...")

    while True:
        conn, addr = s.accept()
        file_request = conn.recv(1024).decode()

        try:
            with open(file_request, 'rb') as f:
                data = f.read(1024)
                while data:
                    conn.send(data)
                    data = f.read(1024)
            print(f"Sent {file_request} to {addr}")
        except FileNotFoundError:
            print(f"File {file_request} not found!")
        finally:
            conn.close()

def download_file(ip, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, 9090))
        s.send(filename.encode())
        
        with open(f"downloaded_{filename}", 'wb') as f:
            data = s.recv(1024)
            while data:
                f.write(data)
                data = s.recv(1024)
        print(f"Downloaded {filename} as downloaded_{filename}")

def request_file_from_server(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 8080))
        s.send(filename.encode())

        response = pickle.loads(s.recv(1024))
        
        if response['status'] == 'found':
            print(f"File {response['filename']} found on client {response['client_ip']}")
            decision = input("Do you want to download it? (yes/no): ")
            if decision == 'yes':
                download_file(response['client_ip'], response['filename'])
        else:
            print("File not found!")
'''
def login(username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 8080))
        msg = str("login,"+username+','+password)
        s.send(msg.encode())

        response = pickle.loads(s.recv(1024))
        if response['status'] == 'True':
            print("Successfully login")
        else: print("Fuck you bastard")


def register(username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 8080))
        msg = str("register,"+username+','+password)
        s.send(msg.encode())

        response = pickle.loads(s.recv(1024))
        if response['status'] == 'True':
            print("Successfully registered")
        else: print("Fuck you bastard")


f1 = input("Type in your username:")
f2 = input("Type in your password:")
login(f1, f2)
