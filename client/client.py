import socket
import json
import time
import os

# socket.MSG_DONTWAIT


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

    def get_list_files(self):
        list_files = ""
        permission_get = True
        self.client_socket.send(b'list_files')
        while permission_get:
            get_list_files = self.client_socket.recv(10).decode()
            if get_list_files == 'END':
                break
            list_files += get_list_files
        return list_files


# get-file: | list-files:  | connect : OK | terminate : OK | help : OK| create a directory Download for files if not exists
