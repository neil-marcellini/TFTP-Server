import socket
HOST = ''
PORT = 6969

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("TFTP Server Listening")
    while True:
        data, addr = s.recvfrom(1024)
        opcode = int.from_bytes(data[:2], byteorder='big')
        print(f"opcode = {opcode}")
