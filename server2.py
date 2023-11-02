import socket
import threading

HEADER = 64 
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
print(ADDR)

clients = {}

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int (msg_length)
            message = client.recv(msg_length).decode(FORMAT)
            print(message)
            if message == DISCONNECT_MESSAGE:
                print("Disconnect")
                connected = False
            elif message.startswith('publish'):
                _, lname, fname = message.split()
                clients[addr] = clients.get(addr, []) + [(lname, fname)]
                print("File_sharing have been updated")
                note = "File_sharing have been updated"
                notify = note.encode(FORMAT)
                notify_lenght = len(notify)
                send_length = str(notify_lenght).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                client.send(send_length)
                client.send(notify)
                print(clients)
            elif message.startswith('fetch'):
                _, fname = message.split()
                holder_addresses = [addr for addr, files in clients.items() if any(f[1] == fname for f in files)]
                response = ', '.join(map(str, holder_addresses))
                notify = response.encode(FORMAT)
                notify_lenght = len(notify)
                send_length = str(notify_lenght).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                client.send(send_length)
                client.send(notify)
    client.close()
            
def start_server():
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count()-1} /n")

def cmd_check(cmd):
    try:
        _, ip, port = cmd.split()
    except:
        return False

def ping(admin,ip,port):
    port = int(port)
    address = (ip,port)
    print(address)
    for i in range(3):
        try:
            admin.connect(address)
            return 1
        except Exception as e:
            print(e)
    return 0

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind(ADDR)
    server.listen()
except:
    print("Socket error")
print("Server started.")
server_thread = threading.Thread(target=start_server)
server_thread.start()


# admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Admin started.")


# try:
#     admin.connect(ADDR)
# except socket.error as error:
#     print(f"Can't connect between server-server: {error}")
while True:
    admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Admin started.")
    cmd = input("Enter command (type 'help' for available commands): ")
    if cmd == 'help':
        print("discover [hostname]: discover the list of local files of the host named hostname\n" + "ping [hostname]: live check the host named hostname")
    
#==========================================================================================================================
    elif cmd.startswith('discover'):
        try:
            _, ip, port = cmd.split()
        except:
            print('Invalid command! Please input ip and port\n')
            continue
        connection = ping(admin,ip,port)
        if connection == 0: print('Client offline\n')
        elif connection == 1: 
            print('Client online\n')
            discover = 'discover'.encode(FORMAT)
            cmd_length = len(discover)
            senddiscover_length = str(cmd_length).encode(FORMAT)
            senddiscover_length += b' ' * (HEADER - len(discover))
            
            admin.send(senddiscover_length)
            admin.send(discover)
            
        else: print('Invalid command! Please input ip and port\n')
        admin.close()
#==============================================================================================================================
    elif cmd.startswith('ping'):
        try:
            _, ip, port = cmd.split()
        except:
            print('Invalid command! Please input ip and port\n')
            continue
        connection = ping(admin,ip,port)
        if connection == 0: print('Client offline\n')
        else: print('Client online\n')
        admin.close()
#====================================================================================================================
    elif cmd.startswith('exit'):
        admin.close()
        server.close()
        break
    else:
        print("Command not supported")