#consider cho ping voi discover, khi nao thi mo socket

def ping(self, ip):
    for i in range(0, 3):
        try:
            self.server_socket.connect(ip)
           #self.close()
            return True
        except Exception as e:
            pass
    return False

def discover(ip):
    if not ping(ip): 
        return False
    self.server_socket.listen(1)

    conn, addr = s.accept()
    num_files = int(conn.recv(1024).decode())
        
        #list nay de nhan ten file
    filenames = []

    num_files = int(conn.recv(1024).decode()) 

    for i in range(num_files):
        filename = conn.recv(1024).decode()
        filenames.append(filename)
        
    conn.close()
    return True
