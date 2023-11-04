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
    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password=password,
                                database = DBName)
    print(f'Connect successfull')
except:
    print('Can\'t connect to MySQL' )
mycursor = mydb.cursor()
mycursor.execute(f"""CREATE TABLE IF NOT EXISTS {User_Table1}(username VARCHAR(255) PRIMARY KEY,password VARCHAR(255),ip VARCHAR(255), port INT, port_for_server INT, status INT)""")
mycursor.execute(f"""CREATE TABLE IF NOT EXISTS {User_Table2}(ip VARCHAR(255), port_for_peer INT, local_name VARCHAR(255),file_name VARCHAR(255) PRIMARY KEY)""")
#=========================================================================================================================================================================================

#====================================================================QUERY IN DATABASE====================================================================================================================
def getAccountByUsername(user):
    mycursor.execute(f"""SELECT * FROM account WHERE username='{user}'""")
    records = mycursor.fetchall()
    return records
def insertUser(user,passwd,ip,port,port_for_server):
    mycursor.execute(f"""INSERT INTO account (user_name,password,ip,port,port_for_server) VALUES ('{user}','{passwd}','{ip}','{port}','{port_for_server}')""")
    mydb.commit()
def insertFile(ip,port,lname,fname):
    mycursor.execute(f"""INSERT INTO file_sharing (ip,port_for_peer,local_name,file_name) VALUES ('{ip}','{port}','{lname}','{fname}')""")
    mydb.commit()

def getAccountByUsernameAndPassword(user,passwd):
    mycursor.execute(f"""SELECT * FROM account WHERE username='{user}' AND password='{passwd}'""")
    records = mycursor.fetchall()
    return records
def updateUser(user,ip,port,status):
    mycursor.execute(f"""UPDATE account SET status={status},ip='{ip}',port='{port}' WHERE username='{user}'""")
    mydb.commit()
def getIpAndPorforServer(user):
    mycursor.execute(f"""SELECT ip,port_for_server FROM account WHERE username='{user}'""")
    records = mycursor.fetchall()
    return records
##########################################################################################################

################################ TRY TO COOK ############################################

def getIPAndPortforPeerwhileFetch(fname):
    mycursor.execute(f"""SELECT ip,port_for_peer FROM file_sharing WHERE (file_name='{fname}')""")
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
    
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int (msg_length)
            message = client.recv(msg_length).decode(FORMAT)
            print(f'Client says: {message}')
            port_for_peer = "5353"  
            if message == DISCONNECT_MESSAGE:
                print("Disconnect")
                connected = False
#=======================================REGISTER=============================================
            elif message.startswith('register'):
                ip,port = addr[0],addr[1]
                user_length = int(client.recv(HEADER).decode(FORMAT))
                user = client.recv(user_length).decode(FORMAT)
                passwd_length = int(client.recv(HEADER).decode(FORMAT))
                passwd = client.recv(passwd_length).decode(FORMAT) 
                record = getAccountByUsername(user)
                port_in4_length = int(client.recv(HEADER).decode(FORMAT))
                port_in4 = client.recv(port_in4_length).decode(FORMAT)
                port_for_server = port_in4
                if record != []:
                    sendMessage(client, "Account has been used - 0")    
                else:
                    try:
                        insertUser(user,passwd,ip,port,port_for_server)
                        sendMessage(client, "200")
                        sendMessage(client, "Account created successfully - 1")
                    except:
                        sendMessage(client, "404")
                        sendMessage(client, "Error. Try again...")
#==========================================LOGIN============================================
            elif message.startswith('login'):
                ip,port = addr[0],addr[1]
                user, passwd = "", ""
                user_length = int(client.recv(HEADER).decode(FORMAT))
                user = client.recv(user_length).decode(FORMAT)
                passwd_length = int(client.recv(HEADER).decode(FORMAT))
                passwd = client.recv(passwd_length).decode(FORMAT) 
#=====================================Moi sua=======================================
                port_for_peer_length = int(client.recv(HEADER).decode(FORMAT))
                port_for_peer = client.recv(port_for_peer_length).decode(FORMAT) 
#===================================================================================
                print(user)
                record = getAccountByUsernameAndPassword(user,passwd)
                print(f"Record: {record}")
                if record == []:
                    sendMessage(client, "Tài khoản hoặc mật khẩu không tồn tại - 0")
                else:
                    try:
                        updateUser(user,ip,port,1)
                        sendMessage(client, "200")
                        sendMessage(client, "Kết nối thành công - 1")
                        sendMessage(client, f'Hello {user}! Welcome to our journey')
                    except Exception as e:
                        sendMessage(client, "404")
                        sendMessage(client, "Lỗi truy vấn. Đang thử lại... - 0")
                        traceback.print_exc()
#=============================================LOGOUT===============================================
            elif message.startswith('logout'):
                ip = addr[0]
                _, user = message.split()
                updateUser(user,ip,port,0)      
#=====================================================================================================                       
            elif message.startswith('publish'):
                _, lname, fname = message.split()
                # clients[addr] = clients.get(addr, []) + [(lname, fname)]
                ip = addr[0]
                print(port_for_peer)
                try:
                    insertFile(ip,port_for_peer,lname,fname)
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
                    response = str(record[0]) + " " + str(record[1])
                    print(response)
                    sendMessage(client=client, message=response)
    client.close()
##########################################################################################################
            
def start_server():
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
        updateUser(user=hostname,ip=ip,port=port,status=0)
    else: 
        print('Client online\n')
        updateUser(user=hostname,ip=ip,port=port,status=1)
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
        updateUser(user=hostname,ip=ip,port=port,status=0)
    elif connection == 1: 
        print('Client online\n')
        updateUser(user=hostname,ip=ip,port=port,status=1)
        discover = 'discover'.encode(FORMAT)
        cmd_length = len(discover)
        senddiscover_length = str(cmd_length).encode(FORMAT)
        senddiscover_length += b' ' * (HEADER - len(discover))
        
        admin.send(senddiscover_length)
        admin.send(discover)
        discover_length = int(admin.recv(HEADER).decode(FORMAT))
        discover_data = discover.recv(discover_length).decode(FORMAT)
        print(discover_data)
    else: print('Invalid command! Please input ip and port\n')
    admin.close()

#----------------------------------------------------------------



if __name__ == "__main__":

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        server.bind(ADDR)
        server.listen()
    except:
        print("Socket error")
    print("Server started.")
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
            server.close()
    #======================================================================================================
        else:
            print("Command not supported")