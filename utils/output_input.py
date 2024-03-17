from colorama import Style


def _print(text: str, color: str) -> None:
    print(color + text + Style.RESET_ALL)


def _input(text: str, color: str) -> None:
    enter = input(color + text + Style.RESET_ALL)
    return enter
