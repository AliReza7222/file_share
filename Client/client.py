import socket, json

history=list()
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    command = input("please enter your command: ").split()
    history.append(command[0])
    if command[0].lower() == 'connect':
        ip, port = command[1], command[2]
        soc.connect((ip, port))
    elif command[0].lower() == "terminate":
        soc.close()
        break
    elif command[0].lower() == 'update' :
        if 'connect' in history:
            message = json.loads(soc.recv(1024))

        else:
            raise Exception("don't connect with server.")


