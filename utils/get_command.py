from colorama import Fore

from .output_input import _input


def get_command() -> tuple:
    input_user = list()
    command = _input("Please enter your command: ", Fore.YELLOW).split()
    if len(command) > 1:
        input_user.extend(command[1:])
    return command[0], input_user
