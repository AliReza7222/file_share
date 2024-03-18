import os
import threading
import socket
import json

from colorama import Fore
from database import DataBase
from utils.exception import BlockIPException
from utils.output_input import (_print, _input)


class Server:

    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 7222
        self.database = DataBase()

    def filter_check_data(self, table_name: str, column: str, data: str) -> bool:
        filter_data = self.database.select_data(
            table_name=table_name,
            column=column,
            condition=f"{column}=\'{data}\'"
        )
        return True if filter_data else False

    def unblock(self, ip: str) -> None:
        if self.filter_check_data(table_name='black_list', column='ip', data=ip):
            self.database.delete_data(
                table_name='black_list',
                data=ip,
                column='ip'
            )
            _print(f"Successfully ip {ip} unblocked .", Fore.GREEN)
        else:
            _print("This ip isn't in black list !", Fore.RED)

    def block(self, ip: str) -> None:
        if not self.filter_check_data(table_name='black_list', column='ip', data=ip):
            self.database.insert_data(
                table_name='black_list',
                columns='ip',
                data=f"\'{ip}\'")
            _print(f"Successfully block ip {ip}", Fore.GREEN)
        else:
            _print(f"Ip {ip} exists in black list", Fore.RED)

    def list_files(self):
        return self.database.select_data(table_name='media', column="name, file")

    def add_file(self, name: str, path_file: str) -> None:
        if not self.filter_check_data(table_name='media', column='name', data=name):
            self.database.insert_data(
                table_name='media',
                columns='name, file',
                data=f"\'{name}\', \'{path_file}\'"
            )
            _print(f"Successfully add file {name} .", Fore.GREEN)
        else:
            _print(f"A file with this name: {name} exists !", Fore.RED)

    def remove_file(self, name_file: str):
        if self.filter_check_data(table_name='media', column='name', data=name_file):
            self.database.delete_data(
                table_name='media',
                column='name',
                data=f"\'{name_file}\'"
            )
            _print(f"Successfully remove file with name {name_file} .", Fore.GREEN)
        else:
            _print(f"There is no file with this name!", Fore.RED)

    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
            socket_server.bind((self.ip, self.port))
            socket_server.listen(10)
            _print('-'*20 + "server activated" + '-'*20, Fore.CYAN)
            for i in range(1, 10):
                socket_client, address = socket_server.accept()
                th = threading.Thread(target=self.client_handler,
                    args=(socket_client, address), name=f"client{i}")
                th.start()
                _print(f"{address[0]}:{address[1]} connectd !", Fore.GREEN)
            _print("close server !", Fore.RED)

    def check_ip_status(self, ip: str) -> None:
        if self.filter_check_data(table_name='black_list', column='ip', data=ip):
            raise BlockIPException("Your IP is blocked!")

    def client_handler(self, client, address): # not check and clean
        self.check_ip_status(ip=address[0])
        while True:
            message_continue = (client.recv(1000)).decode()
            list_file = list()
            list_addr = list()
            with open("file_list.txt", "r") as all_file:
                files = all_file.read().split()
                list_addr.extend(files)
                for line in files:
                    name_file = line.split("\\")[-1]
                    list_file.append(name_file)
            if message_continue == "update":
                message_list = json.dumps(list_file)
                client.sendall(message_list.encode())
            elif message_continue == "get":
                message_client_one = client.recv(1024).decode()
                if message_client_one in list_addr:
                    name_file_download = message_client_one.split("\\")[-1]
                    with open(message_client_one, "rb") as select_file:
                        file = select_file.read()
                        client.sendall(file)
                    print(f"file {name_file_download} downloaded ." )
            elif message_continue == "terminate":
                print(f"exit {name}.")
                break
