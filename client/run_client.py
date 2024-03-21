import socket

from colorama import Fore

from .client import Client
from utils.output_input import _print, _input
from utils.get_command import get_command


class RunClient(Client):

    def __init__(self):
        self.permission_run = True
        super().__init__()

    def command_user(self) -> None:
        while self.permission_run:
            action, input_user = get_command()
            self.process_command(action, input_user)

    def process_command(self, action: str, input_user: list) -> None:
        if action == 'connect' and len(input_user) == 0:
            if not self.connect_to_server:
                try:
                    message_server = self.connect()
                    if message_server == 'connected':
                        _print("You connected to server .", Fore.LIGHTGREEN_EX)
                    elif message_server == 'reject':
                        _print("Your ip is blocked !", Fore.LIGHTRED_EX)
                except socket.error as error_message:
                    _print(str(error_message), Fore.LIGHTRED_EX)
            else:
                _print("You connect to server !", Fore.LIGHTRED_EX)

        elif action == "help" and len(input_user) == 0:
            with open("client/help_client.txt", "r") as file_help:
                _print(file_help.read(), Fore.CYAN)

        elif action == "exit" and len(input_user) == 0:
            self.exit()
            self.permission_run = False
            _print('Bye :) ', Fore.LIGHTRED_EX)

        elif not self.connect_to_server:
            _print("You are not connect to server please connect to server !", Fore.LIGHTRED_EX)

        elif action == 'list_files' and len(input_user) == 0:
            name_files = self.get_list_files().split(',')
            for name in name_files:
                _print(f"name :\t {name}", Fore.LIGHTBLUE_EX)

        elif action == 'download' and len(input_user) == 1:
            if self.check_file_exists(name_file=input_user[0]):
                _print("Please waite for download file ...", Fore.LIGHTCYAN_EX)
                self.download_file(name_file=input_user[0])
                _print(f"Download file {input_user[0]} successfully completed ✔", Fore.LIGHTGREEN_EX)
            else:
                _print("There is no file with this name !", Fore.LIGHTRED_EX)

        else:
            _print("This command is invalid. Enter 'help' for a list of commands.", Fore.LIGHTRED_EX)


client = RunClient()
client.command_user()
