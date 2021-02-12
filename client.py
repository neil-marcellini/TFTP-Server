import socket
HOST = 'localhost'
PORT = 50007
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello Server.')
    data = s.recv(1024)
    s.close()
    print("Received ", repr(data))