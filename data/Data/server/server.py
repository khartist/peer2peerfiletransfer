import socket
import pickle

clients = {
    '127.0.0.1': ['aoyama.png', 'chino.png', 'chiya.png'],
    '127.0.0.2': ['hlep.txt', 'cocoa.png', 'rize.png'],
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8080))
s.listen(5)

while True:
    conn, addr = s.accept()
    file_request = conn.recv(1024).decode()
    
    file_found = False
    for client_ip, files in clients.items():
        if file_request in files:
            file_found = True
            response = {
                'status': 'found',
                'client_ip': client_ip,
                'filename': file_request
            }
            conn.send(pickle.dumps(response))
            break
            
    if not file_found:
        response = {
            'status': 'not_found'
        }
        conn.send(pickle.dumps(response))
        
    conn.close()
