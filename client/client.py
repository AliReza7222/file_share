import socket, json
import time, os

history = list()
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
list_update = list()
if os.path.exists("Download") == False:
    os.mkdir("Download")

while True:
    command = input("please enter your command: ").split()
    history.append(command[0])
    if command[0].lower() == 'connect':
        ip, port = '127.0.0.1', 72
        soc.connect((ip, port))
        soc.sendall(command[0].encode())
        print("connect to server .")
    elif command[0].lower() == "terminate":
        try:
            history.append("terminate")
            soc.sendall(command[0].encode())
            soc.close()
            break
        except:
            break
    elif command[0].lower() == 'update':
        if 'connect' in history:
            n, s = 0, ''
            while n < 7:
                time.sleep(0.5)
                s += '*'
                print(s, end="")
                n += 1
            soc.sendall(command[0].encode())
            message = json.loads(soc.recv(1024))
            list_update = message
            print("\nsuccessfully list update.")
        else:
            raise Exception("don't connect with server.")
    elif command[0] == "history":
        print(history)
    elif command[0] == "list":
        print(f"list update is:\n{list_update}")
    elif command[0].lower() == 'get' and 'connect' in history:
        soc.sendall(command[0].encode())
        name = command[1].split("\\")[-1]
        if name in list_update:
            soc.sendall(command[1].encode())
            select_file = soc.recv(9000000)
            with open(f"Download\\{name}", "wb") as download:
                n, s = 0, ""
                print("download file ........")
                while n < 7:
                    s += "*"
                    time.sleep(0.7)
                    print(s, end='')
                    n += 1
                download.write(select_file)
            print("\nsuccessfully download.")
    elif command[0].lower() == 'help':
        with open("help.txt", 'r') as help_file:
            print(help_file.read())
    else:
        print("don\'t have command.\n")
        continue
