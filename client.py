import socket 
import threading
import sys

HEADER = 64 
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
HOSTNAME = "Drazod"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int (msg_length)
    msg = conn.recv(msg_length).decode(FORMAT)
    if connected and msg == HOSTNAME:
        print("Hello there!")
    conn.close()


def command(command):
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(ADDR)
    all_words = command.split()
    cmd = all_words[0]
    if cmd == "publish":
        fname = all_words[1] +' '+ all_words[2]
        filename = fname.encode(FORMAT)
        fname_lenght = len(filename)
        send_length = str(fname_lenght).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        client.send(send_length)
        client.send(filename)
    if cmd == "ping":
        exit


def pingresply():
    for message in iter(lambda: s.recv(1024).decode(), ''):
        client.send("receive {message}")

background_thread = threading.Thread(target=pingresply)
background_thread.daemon = True
background_thread.start()

while True:
    s = input("Enter your cmd: ")
    command(s)