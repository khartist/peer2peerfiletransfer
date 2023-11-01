import socket
import pickle
import sqlite3

connection = sqlite3.connect('users.db')

cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS USERS(username text, password text, ip text)"""
command2 = """CREATE TABLE IF NOT EXISTS FILE(file text, ip text)"""


cursor.execute(command1)
cursor.execute(command2)
cursor.execute("INSERT INTO FILE VALUES('127.0.0.1', 'sdfdasf.txt')")
cursor.execute("INSERT INTO USERS VALUES('user1', 'pass1', '127.0.0.1')")
cursor.execute("INSERT INTO USERS VALUES('user2', 'pass2', '127.0.0.2')")
cursor.execute("INSERT INTO USERS VALUES('user3', 'pass3', '127.0.0.1')")
cursor.execute("INSERT INTO USERS VALUES('user4', 'pass4', '127.0.0.2')")
cursor.execute("INSERT INTO USERS VALUES('user5', 'pass5', '127.0.0.1')")
cursor.execute("INSERT INTO USERS VALUES('user6', 'pass6', '127.0.0.2')")

#clients = {
    #'127.0.0.1': ['aoyama.png', 'chino.png', 'chiya.png'],
    #'127.0.0.2': ['hlep.txt', 'cocoa.png', 'rize.png'],
#}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(5)

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

while True:  
    conn, addr = s.accept()
    msg = conn.recv(1024).decode()
    
    user_found = False
    part = msg.split(',')
    cmd = part[0]
    if(cmd == "login"):
        loginService(part[1], part[2])
    elif (cmd == "register"):
        register(part[1], part[2])
    
