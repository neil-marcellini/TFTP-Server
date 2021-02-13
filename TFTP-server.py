import socket
HOST = ''
PORT = 6969

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("TFTP Server Listening")
    file_name_start = 2
    while True:
        data, addr = s.recvfrom(1024)
        byte_data = bytearray(data)
        print(byte_data)
        opcode = int.from_bytes(data[:file_name_start], byteorder='big')
        print(f"opcode = {opcode}")
        if opcode != 1: print("Not a RRQ, closing")
        # get file name
        byte_data = byte_data[file_name_start:]
        null_byte = b'\x00'
        print(f"null_byte = {null_byte}")
        zero_index = byte_data.index(null_byte) + file_name_start
        print(zero_index)
        file_name = data[file_name_start:zero_index]
        file_name = file_name.decode('utf-8')
        print(f"file_name = {file_name}")
            
