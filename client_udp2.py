import os
import socket
import threading
from tzlocal import get_localzone

code_table = 'utf-8'

name = input("Username. No more then 16 symbols: ")
if len(name) > 16:
    print("No more then 16 symbols, try again")
    name = input("Username: ")

hostS = 'networkslab-ivt.ftp.sh'
hostL = '127.0.0.1'
port = 55555
file_end = '37e3f4a8-b8c9-4f22-ad4d-8bd81e686822'
length_of_message = len(f"file{file_end}")
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect((hostL, 55555))
lenght = 65535
making_connection = False


def receive_message():
    while True:
        full_mes = ''.encode(code_table)
        message = ''.encode(code_table)
        message, address = client.recvfrom(lenght)
        full_mes += message
        while not file_end.encode(code_table) in full_mes:
            message, address = client.recvfrom(lenght)
            full_mes += message
        else:
            print(full_mes[:full_mes.find(file_end.encode(code_table))].decode(code_table))
            buffer = 0


def send_message():
    global making_connection
    while True:
        if not making_connection:
            client.sendto(bytearray(1), (hostL, port))
            print(f'client with name {name} connected ')
            making_connection = True
        local_tz = get_localzone()
        message = input("") + file_end
        if message == f"file{file_end}":
            file_name = input("Type file name: ")
            file_size = os.path.getsize(file_name) + len(file_end.encode(code_table))
            client.sendto(f"{message}".encode(code_table), (hostL, port))
            file_name_size = f"{file_name}<>{file_size}".encode()
            client.sendto(f"{len(file_name_size):<{length_of_message}}".encode(code_table), (hostL, port))
            client.sendto(file_name_size, (hostL, port))
            f = open(file_name, "rb")
            file_data_write = f.read(lenght - len(file_end.encode(code_table)) - 1)
            mod_data_to_send = file_data_write + file_end.encode(code_table)
            client.sendto(mod_data_to_send, (hostL, port))
            f.close()
            print(f'File {file_name} is send')
        else:
            message_send = f'<{local_tz}>{name}->{message}'.encode(code_table)
            message_len_send = f'{len(message_send):<{length_of_message}}'.encode(code_table)
            client.sendto(message_len_send + message_send, (hostL, port))


receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

write_thread = threading.Thread(target=send_message)
write_thread.start()
