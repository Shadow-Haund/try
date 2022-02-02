import socket
import threading
from datetime import datetime
from pytz import timezone

code_table = 'utf-8'

hostS = 'networkslab-ivt.ftp.sh'
hostL = '127.0.0.1'
port = 55555
file_end = '37e3f4a8-b8c9-4f22-ad4d-8bd81e686822'
length_of_message = len(f"file{file_end}")

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((hostL, port))
# server.listen()
u_sockets = []
lenght = 65535


def broadcast(message, addres):
    for client in u_sockets:
        # if client != addres:
        server.sendto(message, addres)


# отправлять по адресам, принимать сервером server.recvfrom(lenght)
# отправлять от сервера то есть server.sendto(message, addres). адреса в users


# def handle(message, address):
def handle():
    global u_sockets
    buffer = 0
    full_mes = bytes()
    full_file = bytes()
    while True:
        # try:
        # if buffer == 0:

        message, address = server.recvfrom(lenght)
        message = message.decode(code_table)
        if address not in u_sockets:
            print(f"Connected with {str(address)}")
            u_sockets.append(address)
        # if message.strip().isdigit():  # если число, то это просто сообщение и нужно изменить длину буфера
        #     buffer = int(message.strip())
        # if message == f"file{file_end}":  # если file, то хотят отправить файл
        #     file_header_len, addres = server.recvfrom(lenght)
        #     file_header_len = int(file_header_len.decode())
        #     file_name_size, address = server.recvfrom(lenght)  # заголовок это имя файла и размер файла
        #     file_name_size = file_name_size.decode(code_table)
        #     file_size = file_name_size[file_name_size.find("<>") + 2:]
        #     file_size = int(file_size)
        #     file_data_read, address = server.recvfrom(lenght)
        #     full_file += file_data_read
        #     while not file_end.encode(code_table) in full_file:
        #         file_data_read, address = server.recvfrom(lenght)
        #         full_file += file_data_read
        #     else:
        #         broadcast(f'{f"file{file_end}":<{len(f"file{file_end}".encode(code_table))}}'.encode(code_table) +
        #                   f'{len(file_name_size.encode(code_table)):<{length_of_message}}'.encode(code_table) +
        #                   file_name_size.encode(code_table) + full_file, address)
        #         print("serF2")
        else:
            message, address = server.recvfrom(lenght)
            full_mes += message
            # это часть модернизируется с целью успешного получения всего сообщения при выкладке сервера удаленно
            while not file_end.encode(code_table) in full_mes:
                message, address = server.recvfrom(lenght)
                full_mes += message
            else:
                time_zone = full_mes[
                            full_mes.find('<'.encode(code_table)) + 1: full_mes.find('>'.encode(code_table))]
                now_time = datetime.now(timezone(time_zone)).strftime(
                    "%Y-%m-%d %H:%M")  # время сервера измененное в соответствии с tz пользователя
                message_send = '<'.encode(code_table) + now_time.encode(code_table) + '> '.encode(code_table) \
                               + full_mes[full_mes.find('>'.encode(code_table)) + 1:]
                message_len_send = f'{len(message_send):<{length_of_message}}'.encode(
                    code_table)
                broadcast(message_len_send + message_send, address)
                print("sev2")
                buffer = 0
    # except:
    #     u_sockets.remove(client)
    #     client.close()
    #     break


# thread = threading.Thread(target=handle, args=(dec_message, address))
thread = threading.Thread(target=handle)
thread.start()
# def receive_connection():
#     while True:
#         print("server woking")
#         message, address = server.recvfrom(lenght)
#         dec_message = message.decode(code_table)
#         print(f"Connected with {str(address)}")
#         u_sockets.append(address)
#         thread = threading.Thread(target=handle, args=(dec_message,address))
#         thread.start()
#
#
# receive_connection()
# создавать потоки как в клиенте и так же (предположительно) вызывать handle без recieve вообще
