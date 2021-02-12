import socket
HOST = ''
PORT = 69

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("TFTP Server Listening")
    while True:
        data, addr = sock.recvfrom(1024)
        byte_list = bytearray(data)
        opcode = int.from_bytes(byte_list[:2], byteorder='big')
        print(f"opcode = {opcode}")