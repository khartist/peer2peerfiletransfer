import socket
import threading
import mysql.connector
import traceback

password = input("Enter your password of MySQL: ")
DBName = "PeartoPear"
User_Table1 = "account"
User_Table2 = "file_sharing"
HEADER = 64 
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
print(ADDR)

#============================================CREATE DB AND TABLE =========================================================================================================================
clients = {}
try:
    mydb = mysql.connector.connect(host="localhost",user="root",password=password,database = DBName,auth_plugin='mysql_native_password')
    print(f'Connect successfull')
except:
    print('Can\'t connect to MySQL' )
mycursor = mydb.cursor()
mycursor.execute(f"""CREATE TABLE IF NOT EXISTS {User_Table1}(username VARCHAR(255) PRIMARY KEY,password VARCHAR(255),ip VARCHAR(255), port INT, port_for_server INT, port_for_peer INT, status INT)""")
mycursor.execute(f"""CREATE TABLE IF NOT EXISTS {User_Table2}(user VARCHAR(255), local_name VARCHAR(255),file_name VARCHAR(255) PRIMARY KEY)""")
#=========================================================================================================================================================================================

#====================================================================QUERY IN DATABASE====================================================================================================================
def getAccountByUsername(user):
    mycursor.execute(f"""SELECT * FROM account WHERE username='{user}'""")
    records = mycursor.fetchall()
    return records
def insertUser(user,passwd,ip,port,port_for_server,port_for_peer):
    mycursor.execute(f"""INSERT INTO account (username,password,ip,port,port_for_server, port_for_peer) VALUES ('{user}','{passwd}','{ip}','{port}','{port_for_server}','{port_for_peer}')""")
    mydb.commit()
def insertFile(user,lname,fname):
    mycursor.execute(f"""INSERT INTO file_sharing (user,local_name,file_name) VALUES ('{user}','{lname}','{fname}')""")
    mydb.commit()

def getAccountByUsernameAndPassword(user,passwd):
    mycursor.execute(f"""SELECT * FROM account WHERE username='{user}' AND password='{passwd}'""")
    records = mycursor.fetchall()
    return records
def updateUser(user,ip,port):
    mycursor.execute(f"""UPDATE account SET ip='{ip}',port='{port}' WHERE username='{user}'""")
    mydb.commit()
def updateStatus(user,status):
    mycursor.execute(f"""UPDATE account SET status={status} WHERE username='{user}'""")
    mydb.commit()
def updatePortforServer(user,ip,port,port_for_server,port_for_peer):
    mycursor.execute(f"""UPDATE account SET port_for_server={port_for_server},port_for_peer={port_for_peer},ip='{ip}',port='{port}' WHERE username='{user}'""")
    mydb.commit()
def getIpAndPorforServer(user):
    mycursor.execute(f"""SELECT ip,port_for_server FROM account WHERE username='{user}'""")
    records = mycursor.fetchall()
    return records
def getUserforPublish(ip,port):
    mycursor.execute(f"""SELECT username FROM account WHERE ip='{ip}' AND port='{port}'""")
    records = mycursor.fetchall()
    return records
##########################################################################################################

################################ TRY TO COOK ############################################

def getIPAndPortforPeerwhileFetch(fname):
    mycursor.execute(f"""SELECT ip, port_for_peer
                FROM account a
                JOIN file_sharing fs ON a.username = fs.user
                WHERE a.status = 1 AND fs.file_name = '{fname}'""")
    records = mycursor.fetchall()
    return records

##################################################################
#---------------------------------------------------------------- Send Message to Client  --------------------------------
def sendMessage(client,message):
    notify = message.encode(FORMAT)
    notify_lenght = len(notify)
    send_length = str(notify_lenght).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(notify)
#==================================================================================================================

def handle_client(client, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    Login_status = False
    while connected:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
        except:
            print("Error sending message")
            connected = False
        if msg_length:
            msg_length = int (msg_length)
            try:
                message = client.recv(msg_length).decode(FORMAT)
            except:
                print("Error sending message")
                continue
            print(f'Client says: {message}')
            if message.startswith('exit'):
                print("Disconnect")
                connected = False
#=======================================REGISTER=============================================
            elif message.startswith('register'):
                ip,port = addr[0],addr[1]
                user_length = int(client.recv(HEADER).decode(FORMAT))
                user = client.recv(user_length).decode(FORMAT)
                passwd_length = int(client.recv(HEADER).decode(FORMAT))
                passwd = client.recv(passwd_length).decode(FORMAT)
                try:
                    record = getAccountByUsername(user)
                except:
                    sendMessage(client, "CANNOT ACCESS TO DATABASE")
                    continue
                port_in4_length = int(client.recv(HEADER).decode(FORMAT))
                port_in4 = client.recv(port_in4_length).decode(FORMAT)
                port_for_server = int(port_in4)
                port_for_peer = port_for_server
                if record != []:
                    sendMessage(client, "Account has been used - 0")    
                else:
                    try:
                        insertUser(user,passwd,ip,int(port),port_for_server,port_for_peer)
                        sendMessage(client, "Account created successfully - 1")
                    except Exception as e:
                        print(e)
                        sendMessage(client, "Error. Try again...")
#==========================================LOGIN============================================
            elif message.startswith('login'):
                ip,port = addr[0],addr[1]
                user, passwd = "", ""
                user_length = int(client.recv(HEADER).decode(FORMAT))
                user = client.recv(user_length).decode(FORMAT)
                passwd_length = int(client.recv(HEADER).decode(FORMAT))
                passwd = client.recv(passwd_length).decode(FORMAT) 
                port_in4_length = int(client.recv(HEADER).decode(FORMAT))
                port_in4 = client.recv(port_in4_length).decode(FORMAT)
                port_for_server = int(port_in4)
                port_for_peer = port_for_server
                print(user)
                try:
                    record = getAccountByUsernameAndPassword(user,passwd)
                except:
                    sendMessage(client, "ERROR WHEN ACCESS TO DATABASE")
                    continue
                print(f"Record: {record}")
                if record == []:
                    sendMessage(client, "Tài khoản hoặc mật khẩu không tồn tại - 0")
                else:
                    try:
                        updateUser(user,ip,port)
                        updatePortforServer(user,ip,port,port_for_server,port_for_peer)
                        updateStatus(user,1)
                        sendMessage(client, "Kết nối thành công - 1")
                        sendMessage(client, f'Hello {user}! Welcome to our journey')
                    except Exception as e:
                        sendMessage(client, "Lỗi truy vấn. Đang thử lại... - 0")
                        traceback.print_exc()
#=============================================LOGOUT===============================================
            elif message.startswith('logout'):
                ip,port = addr[0],addr[1]
                try:
                    record = getUserforPublish(ip,port)
                except:
                    print("ERROR WHEN ACCESS TO DATABASE")
                    sendMessage(client, "ERROR WHEN ACCESS TO DATABASE")
                    continue
                if record != []:
                    user_name = record[0][0]
                else:
                    print("ERROR WHEN ACCESS TO DATABASE")
                    sendMessage(client, "ERROR WHEN ACCESS TO DATABASE") 
                    continue
                print(user_name)
                updateUser(user_name,ip,port)
                updateStatus(user_name,0)
                sendMessage(client, "Client have been logout") 
                connected = False
#=====================================================================================================       
            elif message.startswith('publish'):
                try:
                    _, lname, fname = message.split()
                # clients[addr] = clients.get(addr, []) + [(lname, fname)]
                except:
                    print("Please enter lname and fname")
                ip,port = addr[0],addr[1]
                try:
                    record = getUserforPublish(ip,port)
                except:
                    print("ERROR WHEN ACCESS TO DATABASE")
                    sendMessage(client, "ERROR WHEN ACCESS TO DATABASE")
                    continue
                if record != []:
                    user_name = record[0][0]
                else:
                    print("ERROR WHEN ACCESS TO DATABASE")
                    sendMessage(client, "ERROR WHEN ACCESS TO DATABASE") 
                    continue
                print(user_name)
                try:
                    insertFile(user_name,lname,fname)
                    print("File_sharing have been updated")
                    sendMessage(client=client, message="File_sharing have been updated")
                except:
                    sendMessage(client, "Error. Try again...")
#=======================================================================================================
            elif message.startswith('fetch'):
                _, fname = message.split()
                print(fname)
                try:
                    record = getIPAndPortforPeerwhileFetch(fname)
                except Exception as e:
                    print(e)
                    sendMessage(client, "Error. Try again...")
                    continue
                if record == []: 
                    sendMessage(client, "File is not exist or haven\'t shared by other peer")
                else:
                # holder_addresses = [addr for addr, files in clients.items() if any(f[1] == fname for f in files)]
                # response = ', '.join(map(str, holder_addresses))
                    record = record[0]
                    response = f"{record[0]} {record[1]} {fname}" 
                    print(response)
                    sendMessage(client=client, message=response)
            else:
                sendMessage(client=client, message="Command is not supported")
    client.close()
    print(f"[CONNECTION] {addr} have disconnected")
##########################################################################################################
            
def start_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.bind(ADDR)
        server.listen()
    except:
        print("Socket error")
    print("Server started.")
    while True:
        client, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.daemon = True
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
def ping_em(hostname):
    admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    record = getIpAndPorforServer(hostname)
    if record == []:
        print("Tài khoản hoặc mật khẩu không tồn tại - 0")
        return
    else:
        ip,port = record[0][0],record[0][1]
    connection = ping(admin,ip,port)
    if connection == 0: 
        print('Client offline\n')
        updateStatus(hostname,0)
    else: 
        print('Client online\n')
        updateStatus(hostname,1)
    admin.close()

def discover(hostname):
    admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    record = getIpAndPorforServer(hostname)
    if record == []:
        print("Tài khoản hoặc mật khẩu không tồn tại - 0")
        return
    else:
        ip,port = record[0][0],record[0][1]
    connection = ping(admin,ip,port)
    if connection == 0: 
        print('Client offline\n')
        updateStatus(hostname,0)
    elif connection == 1: 
        print('Client online\n')
        updateStatus(hostname,1)
        discover = 'discover'.encode(FORMAT)
        cmd_length = len(discover)
        senddiscover_length = str(cmd_length).encode(FORMAT)
        senddiscover_length += b' ' * (HEADER - len(discover))
        
        admin.send(senddiscover_length)
        admin.send(discover)
        discover_length = int(admin.recv(HEADER).decode(FORMAT))
        discover_data = admin.recv(discover_length).decode(FORMAT)
        print(discover_data)
    else: print('Invalid command! Please input ip and port\n')
    admin.close()

#----------------------------------------------------------------



if __name__ == "__main__":

    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    

    tnk_baka = True
    ########################################### ADMIN    #####################################################################
    while tnk_baka:
        ip,port = "",""
        print("Admin started.")
        cmd = input("Enter command (type 'help' for available commands): ")
        if cmd == 'help':
            print("discover [hostname]: discover the list of local files of the host named hostname\n" + "ping [hostname]: live check the host named hostname")
        
    #==========================================================================================================================
        elif cmd.startswith('discover'):
            try:
                _, hostname = cmd.split()
            except:
                print('Invalid command! Please input ip and port\n')
                continue
            discover(hostname)
    #==============================================================================================================================
        elif cmd.startswith('ping'):
            try:
                _, hostname = cmd.split()
            except:
                print('Invalid command! Please input ip and port\n')
                continue
            ping_em(hostname)
    #====================================================================================================================
        elif cmd.startswith('exit'):
            tnk_baka = False
    #======================================================================================================
        else:
            print("Command not supported")