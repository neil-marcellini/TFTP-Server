import socket
import os
HOST = ''
PORT = 6969

def getFileBytes(file_name):
    # open file as bytes
    with open(file_name, "rb") as text_file:
        # Read the whole file at once
        file_data = text_file.read()
        return file_data

def serve():
    print("waiting for client")
    data, addr = s.recvfrom(1024)
    print("received request")
    opcode = int.from_bytes(data[:file_name_start], byteorder='big')
    print(f"opcode = {opcode}")
    if opcode != rrq_opcode:
        error_message = b'Not a RRQ, closing'
        error = error_opcode.to_bytes(2, byteorder='big') + \
            undefined_error.to_bytes(2, byteorder='big') + \
            error_message + null_byte
        s.sendto(error, addr)
        data, addr = s.recvfrom(1024)
        return

    # get file name
    zero_index = data[file_name_start:].index(null_byte) + file_name_start
    file_name = data[file_name_start:zero_index]
    file_name = file_name.decode('utf-8')
    print(f"file_name = {file_name}")

    #check if file exists
    file_exists = os.path.exists('./' + file_name)
    if not file_exists:
        print("file not found")
        error_message = b'File not found'
        error = error_opcode.to_bytes(2, byteorder='big') + \
            file_not_found_error.to_bytes(2, byteorder='big') + \
            error_message + null_byte
        s.sendto(error, addr)
        data, addr = s.recvfrom(1024)
        return
    else:
        block_num = 1
        file_data = getFileBytes(file_name)
        data_index = 0
        while data_index < len(file_data):
            # send 512 bytes
            block_data = file_data[data_index:(data_index + block_size)]
            data_packet = data_opcode.to_bytes(2, byteorder='big') + block_num.to_bytes(2,
                    byteorder='big') + block_data
            s.sendto(data_packet, addr)
            # wait for ACK
            print("Waiting for ACK")
            data, addr = s.recvfrom(1024)
            print("Received ACK")
            opcode = int.from_bytes(data[:block_num_start], byteorder='big')
            ack_block_num = int.from_bytes(data[block_num_start:], byteorder='big')
            if opcode != ack_opcode or ack_block_num != block_num:
                print("Invalid ACK or block_num")
            else:
                block_num += 1
                data_index += block_size


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("TFTP Server Listening")
    file_name_start = 2
    block_num_start = file_name_start
    null_byte = b'\x00'
    rrq_opcode = 1
    ack_opcode = 4
    data_opcode = 3
    error_opcode = 5
    undefined_error = 0
    file_not_found_error = 1
    block_size = 512
    while True:
        serve()






            

        
