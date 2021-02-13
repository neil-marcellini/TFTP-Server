import socket
HOST = ''
PORT = 6969

def getFileBytes(file_name):
    # open file as bytes
    with open(file_name, "rb") as text_file:
        # Read the whole file at once
        file_data = text_file.read()
        return file_data


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
        if opcode != 1:
            print("Not a RRQ, closing")
            break

        # get file name
        byte_data = byte_data[file_name_start:]
        null_byte = b'\x00'
        zero_index = byte_data.index(null_byte) + file_name_start
        file_name = data[file_name_start:zero_index]
        file_name = file_name.decode('utf-8')
        print(f"file_name = {file_name}")

        ack_opcode = 4
        block_num = 0
        file_data = getFileBytes(file_name)

        block_size = 512
        data_index = 0
        while data_index < len(file_data):
            block_num += 1
            # send 512 bytes
            block_data = file_data[data_index:(data_index + block_size)]
            data_opcode = 3
            data_packet = data_opcode.to_bytes(2, byteorder='big') + block_num.to_bytes(2,
                    byteorder='big') + block_data
            s.sendto(data_packet, addr)
            # wait for ACK
            print("Waiting for ACK")
            data, addr = s.recvfrom(1024)
            print("Received ACK")
            print(f"data = {data}")
            block_num_start = file_name_start
            opcode = int.from_bytes(data[:block_num_start], byteorder='big')
            print(f"ack opcode = {opcode}")
            ack_block_num = int.from_bytes(data[block_num_start:], byteorder='big')
            print(f"ack_block_num = {ack_block_num}")
            if opcode != ack_opcode or ack_block_num != block_num:
                print("Invalid ACK")
                break
            data_index += block_size





                

            
