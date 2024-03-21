import socket
import json
import time

from colorama import Fore

from utils.output_input import _print
from .database import DataBase


class HandleClient:

    def __init__(self):
        self.database = DataBase()
        self.connect = True

    def speak_with_client(self, client_socket: socket.socket) -> None:
        while self.connect:
            message_client = (client_socket.recv(100)).decode()
            client_ip, client_port = client_socket.getpeername()
            self.process_message_client(
                message_client=message_client,
                client_socket=client_socket,
                ip=client_ip,
                port=client_port
            )

    @staticmethod
    def end_send_data(client_socket: socket.socket) -> None:
        time.sleep(0.001)
        client_socket.send(b'END')  # end send data

    def process_message_client(
            self, message_client: str, client_socket: socket.socket, ip: str, port: str) -> None:
        if message_client == 'exit':
            self.connect = False
            _print(f"{ip}:{port} disconnect !", Fore.RED)

        elif message_client == 'list_files':
            list_files = self.database.select_data(table_name='media', column='name')
            name_files = ','.join([file[0] for file in list_files])
            client_socket.sendall(name_files.encode())
            self.end_send_data(client_socket)
            _print(f"{ip}:{port} get list files .", Fore.GREEN)

        elif message_client == 'check_name_file':
            name_file = client_socket.recv(1000).decode()
            if self.database.filter_check_data(
                    table_name='media', column='name', data=name_file):
                client_socket.send(b'ok')
            else:
                client_socket.send(b'reject')

        elif message_client == 'download':
            name_file = client_socket.recv(1000).decode()
            get_file_from_db = self.database.select_data(
                table_name='media',
                column='file',
                condition=f"name=\'{name_file}\'"
            )
            path_file = get_file_from_db[0][0]
            format_file = path_file.split('/')[-1].split('.')[1]
            client_socket.send(format_file.encode())
            with open(path_file, 'rb') as file:
                byte_file = file.read()
                client_socket.sendall(byte_file)
                self.end_send_data(client_socket)
            _print(f"{ip}:{port} download file {name_file} .", Fore.GREEN)


