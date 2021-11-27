import socket, json

history=list()
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
list_update = list()
while True:
    command = input("please enter your command: ").split()
    history.append(command[0])
    if command[0].lower() == 'connect':
        history.append('connect')
        ip, port = command[1], int(command[2])
        soc.connect((ip, port))
    elif command[0].lower() == "terminate":
        history.append("terminate")
        soc.close()
        break
    elif command[0].lower() == 'update' :
        if 'connect' in history:
            history.append("update")
            message = json.loads(soc.recv(1024))
            list_update = message

        else:
            raise Exception("don't connect with server.")
    elif command[0] == "history":
        print(history)
    elif command[0] == 'get' and 'connect' in history:
        pass


