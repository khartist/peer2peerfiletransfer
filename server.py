import socket
import pickle
import sqlite3

connection = sqlite3.connect('users.db')

cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS USERS(username text, password text)"""
command2 = """CREATE TABLE IF NOT EXISTS FILES(ip text, file text)"""

cursor.execute(command1)
cursor.execute(command2)
cursor.execute("INSERT INTO FILES VALUES('0.0.0.0', 'a.txt')")
cursor.execute("INSERT INTO FILES VALUES('1.1.1.1', 'v.jpeg')")
cursor.execute("INSERT INTO FILES VALUES('2.2.2.2', 'l.png')")
cursor.execute("INSERT INTO FILES VALUES('3.3.3.3', 'g.jpg')")
cursor.execute("INSERT INTO FILES VALUES('4.4.4.4', 'e.pptx')")
cursor.execute("INSERT INTO FILES VALUES('5.5.5.5', 'f.pdf')")
cursor.execute("INSERT INTO USERS VALUES('user1', 'pass1')")
cursor.execute("INSERT INTO USERS VALUES('user2', 'pass2')")
cursor.execute("INSERT INTO USERS VALUES('user3', 'pass3')")
cursor.execute("INSERT INTO USERS VALUES('user4', 'pass4')")
cursor.execute("INSERT INTO USERS VALUES('user5', 'pass5')")
cursor.execute("INSERT INTO USERS VALUES('user6', 'pass6')")

#clients = {
    #'127.0.0.1': ['aoyama.png', 'chino.png', 'chiya.png'],
    #'127.0.0.2': ['hlep.txt', 'cocoa.png', 'rize.png'],
#}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(5)

#query into user table
def getUserTable():
    cursor.execute("SELECT * FROM USERS")
    results = cursor.fetchall()
    for result in results:
        print(result)
    return results

#login
def authethicationLogin(username, password):
    results = getUserTable()
    for result in results:
        if(result[0] == username and result[1] == password):
            print("Correct bro")
            return True
    print("False lmao")
    return False

def loginService(username, password):
    state = authethicationLogin(username, password)
    if state == False:
        respone = {
            'status': 'False'
        }
        conn.send(pickle.dumps(respone))
    else: 
        respone = {
            'status': 'True'
        }
        conn.send(pickle.dumps(respone))

#register
def register(username, password):
    cursor.execute("INSERT INTO USERS VALUE(?, ?)", (username, password))
    print(f"{username} has succesfully registered")

#query voi file list
def getFileList():
    cursor.execute("SELECT * FROM FILES")
    results = cursor.fetchall()
    file_list = []
    for result in results:
        ip = result[0]
        file = result[1]
        file_list.append((ip, file))
    return file_list

def getIPList():
    cursor.execute("SELECT ip FROM FILES")
    results = cursor.fetchall()
    ip_set = set()
    for result in results:
        ip_set.add(result)
    unique_ip = list(ip_set)
    return unique_ip

def getFileFromList(name):
    results = getFileList()
    for result in results:
        if(name == result[2]):
            print("Find that file in db")
            return True
    print("Sorry, can not find that file in db")
    return False

def createNewFileLog(ip ,name):
    cursor.execute("INSERT INTO FILES VALUE(?, ?)", (ip, name))
    print(f"{ip}'s repo has succesfully registered")

def findFileByIP(ip):
    cursor.execute("SELECT file FROM FILES WHERE ip = ?", (ip))
    result = cursor.fetchall()
    if result is None:
        print("Cannot find anything bro")
        return result
    print(f"Oh there is something in this address {ip}\n")
    return result

def discover(ip):
    #goi ham discover tu ben Client, tra ve server, server nhan list nay, sau do chuyen len UI
    return {'a.txt','b.pdf','c.docx','d.pdf','e.pptx', 'f.txt', 'm.txt', 'xxx.txt', 'lol.exe', 'ciscoPacketTrace.txt', 'yyy.txt'}

def ping(ip):
    return True

'''while True:  
    conn, addr = s.accept()
    msg = conn.recv(1024).decode()
    
    user_found = False
    part = msg.split(',')
    cmd = part[0]
    if(cmd == "login"):
        loginService(part[1], part[2])
    elif (cmd == "register"):
        register(part[1], part[2])
    '''
