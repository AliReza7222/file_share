import socket, json
import time

history=list()
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
list_update = list()
while True:
    command = input("please enter your command: ").split()
    history.append(command[0])
    if command[0].lower() == 'connect':
        history.append('connect')
        ip, port = '127.0.0.1', 72
        soc.connect((ip, port))
        print("connect to server .")
    elif command[0].lower() == "terminate":
        history.append("terminate")
        soc.close()
        break
    elif command[0].lower() == 'update' :
        if 'connect' in history:
            n, s = 0, ''
            history.append("update")
            while n<7:
                time.sleep(0.5)
                s += '*'
                print(s, end="")
                n += 1
            message = json.loads(soc.recv(1024))
            list_update = message
            print("\nsuccessfully list update.")
        else:
            raise Exception("don't connect with server.")
    elif command[0] == "history":
        print(history)
    elif command[0] == "list":
        print(f"list update is:\n{list_update}")
    elif command[0] == 'get' and 'connect' in history:
        name = command[1].split("\\")[-1]
        if name in list_update:
            soc.sendall(command[1].encode())
            select_file = soc.recv(900000)
            with open(f"..\Download\\{name}","wb") as download:
                n, s = 0, ""
                print("download file ........")
                while n<7:
                    s += "*"
                    time.sleep(0.7)
                    print(s, end='')
                    n += 1
                download.write(select_file)
            print("\nsuccessfully download.")
    else:
        print("don\'t have command.\n")
        continue


