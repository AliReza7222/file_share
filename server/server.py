import threading
import socket

from colorama import Fore
from .database import DataBase
from .handle_client import HandleClient
from utils.output_input import _print


class Server:

    def __init__(self):
        self.ip = '127.0.0.1'
        self.port = 7222
        self.database = DataBase()
        self.client = HandleClient()

    def unblock(self, ip: str) -> None:
        if self.database.filter_check_data(table_name='black_list', column='ip', data=ip):
            self.database.delete_data(
                table_name='black_list',
                data=ip,
                column='ip'
            )
            _print(f"Successfully ip {ip} unblocked .", Fore.GREEN)
        else:
            _print("This ip isn't in black list !", Fore.RED)

    def block(self, ip: str) -> None:
        if not self.database.filter_check_data(table_name='black_list', column='ip', data=ip):
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
        if not self.database.filter_check_data(table_name='media', column='name', data=name):
            self.database.insert_data(
                table_name='media',
                columns='name, file',
                data=f"\'{name}\', \'{path_file}\'"
            )
            _print(f"Successfully add file {name} .", Fore.GREEN)
        else:
            _print(f"A file with this name: {name} exists !", Fore.RED)

    def remove_file(self, name_file: str):
        if self.database.filter_check_data(table_name='media', column='name', data=name_file):
            self.database.delete_data(
                table_name='media',
                column='name',
                data=name_file
            )
            _print(f"Successfully remove file with name {name_file} .", Fore.GREEN)
        else:
            _print(f"There is no file with this name!", Fore.RED)

    def check_ip_blocked(self, ip: str, port: int, client_socket: socket.socket) -> bool:
        if self.database.filter_check_data(table_name='black_list', column='ip', data=ip):
            _print("This Ip is blocked for connection !", Fore.RED)
            client_socket.sendall('reject'.encode())
            return True
        _print(f"{ip}:{port} connected !", Fore.GREEN)
        client_socket.sendall(f'connected'.encode())
        return False

    def start(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
                socket_server.bind((self.ip, self.port))
                socket_server.listen(10)
                _print('-'*20 + "server activated" + '-'*20, Fore.CYAN)
                for i in range(1, 10):
                    client_socket, address = socket_server.accept()  # Waiting for a connection
                    if self.check_ip_blocked(ip=address[0], port=address[1], client_socket=client_socket):
                        continue
                    th = threading.Thread(
                        target=self.client.speak_with_client,
                        args=(client_socket, ),
                        name=f"client{i}")
                    th.start()
                _print("close server !", Fore.RED)
        except socket.error as error_message:
            _print(str(error_message), Fore.RED)
