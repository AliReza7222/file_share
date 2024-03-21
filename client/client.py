import socket
import json
import time
import os


class Client:

    def __init__(self):
        self.connect_to_server = False
        self.client_socket = None

    def connect(self) -> str:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 7222))
        message_server = self.client_socket.recv(20).decode()
        if message_server == 'connected':
            self.connect_to_server = True
        elif message_server == 'reject':
            self.client_socket.close()
        return message_server

    def exit(self) -> None:
        if self.connect_to_server:
            self.client_socket.send(b"exit")
            self.client_socket.close()

    def get_data(self) -> bytes:
        data = b''
        permission_get = True
        while permission_get:
            get_list_files = self.client_socket.recv(4 * 10**6)
            if get_list_files == b'END':
                break
            data += get_list_files
        return data

    def get_list_files(self) -> str:
        self.client_socket.send(b'list_files')
        return self.get_data().decode()

    def check_file_exists(self, name_file: str) -> bool:
        """" check file exists with name : name_file for download """
        self.client_socket.send(b'check_name_file')
        self.client_socket.send(name_file.encode())
        message_server = self.client_socket.recv(10).decode()
        if message_server == 'ok':
            return True
        elif message_server == 'reject':
            return False

    @staticmethod
    def check_exists_dir_download():
        if not os.path.exists('Download'):
            os.mkdir('Download')

    def download_file(self, name_file: str) -> None:
        self.client_socket.send(b'download')
        self.client_socket.send(name_file.encode())
        format_file = self.client_socket.recv(100).decode()
        byte_file = self.get_data()
        self.check_exists_dir_download()
        with open(f"Download/{name_file}.{format_file}", 'wb') as file:
            file.write(byte_file)
