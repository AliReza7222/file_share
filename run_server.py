import time
import threading
from colorama import Fore

from server import Server
from utils.output_input import _print, _input


class RunServer(Server):

    def __init__(self):
        self.permission_run = True
        super().__init__()

    def command_user(self) -> None:
        if self.database.check_exists_db():
            while self.permission_run:
                input_user = list()
                time.sleep(0.5)
                command = _input("Please enter your command: ", Fore.YELLOW).split()
                if len(command) > 1:
                    input_user = command[1:]
                self.process_command(action=command[0], input_user=input_user)
        else:
            _print("Please Create Your database !", Fore.RED)

    def process_command(self, action: str, input_user: list) -> None:
        if action == 'start' and len(input_user) == 0:
            self.start()

        elif action == "list_files" and len(input_user) == 0:
            files = self.list_files()
            for file in files:
                _print(f"name : {file[0]} \t|\t path: {file[1]}", Fore.BLUE)

        elif action == "add_file" and len(input_user) == 2:
            threading.Thread(
                target=self.add_file, args=(input_user[0], input_user[1])).start()

        elif action == "remove_file" and len(input_user) == 1:
            threading.Thread(target=self.remove_file, args=(input_user[0], )).start()

        elif action == "ban" and len(input_user) == 1:
            self.block(ip=input_user[0])

        elif action == "unban" and len(input_user) == 1:
            self.unblock(ip=input_user[0])

        elif action == "help" and len(input_user) == 0:
            with open("help_server.txt", "r") as file_help:
                _print(file_help.read(), Fore.CYAN)

        elif action == "exit" and len(input_user) == 0:
            self.permission_run = False
            _print('Bye :) ', Fore.RED)

        else:
            print(action, input_user)
            _print("This command is invalid. Enter 'help' for a list of commands.", Fore.RED)


obj = RunServer()
obj.command_user()
