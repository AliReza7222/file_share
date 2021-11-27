import threading, socket, json, time


class Server:
    list_ban = list()

    def __init__(self):
        pass

    def client_handler(self, client, address):
        if address[0] not in self.list_ban:
            list_file = list()
            list_addr = list()
            with open("..\\file_list.txt","r") as all_file:
                files = all_file.read().split()
                list_addr = files
                for line in files:
                    name_file = line.split("\\")[-1]
                    list_file.append(name_file)
            message_list = json.dumps(list_file)
            client.sendall(message_list.encode())
            try:
                message_client_one = client.recv(1024).decode()
                if message_client_one in list_addr:
                    with open(message_client_one,"rb") as select_file:
                        file = select_file.read()
                        client.sendall(file)
            except:
                pass

    def start(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip, port = '127.0.0.1', 72
        soc.bind((ip, port))
        soc.listen(10)
        print("active server .")
        for i in range(1, 10):
            s_c, address = soc.accept()
            print(f"connect client {i}.....")
            th = threading.Thread(target=self.client_handler, args=(s_c, address), name=f"client{i}")
            th.start()
        soc.close()
        print("close server.")

    def ban(self, ip, un=None):
        if ip not in self.list_ban:
            self.list_ban.append(ip)
        if un == 'yes' and ip in self.list_ban:
            self.list_ban.remove(ip)
        return self.list_ban

    def add_file(self, address_file):
        with open("..\\file_list.txt", 'r+') as all_file:
            try:
                list_files = all_file.read().split()
                if address_file not in list_files and len(list_files)>0:
                    all_file.write(f"\n{address_file}")
                elif address_file not in list_files and len(list_files)==0:
                    all_file.write(address_file)
                print("add file in file_list.")
            except:
                print("Error add_file.")

    def remove_file(self, address):
        with open("..\\file_list.txt", 'r+') as all_file:
            list_file = all_file.read().split()
            if address in list_file:
                list_file.remove(address)
            print("file remove of list.")

    def start_manager(self):
        while True:
            time.sleep(0.5)
            command = input("Please enter your command: ").split()
            if command[0].lower() == 'start':
                threading.Thread(target=self.start()).start()
            elif command[0].lower() == "terminate":
                break
            elif command[0].lower() == "add_file":
                threading.Thread(target=self.add_file, args=(command[1],)).start()
            elif command[0].lower() == "remove_file":
                threading.Thread(target=self.remove_file, args=(command[1],)).start()
            elif command[0].lower() == "ban":
                threading.Thread(target=self.ban, args=(command[1],)).start()
            elif command[0].lower() == "unban":
                threading.Thread(target=self.ban, args=(command[1], 'yes')).start()
            elif command[0].lower() == "help":
                with open("..\\help.txt", "r") as file_help:
                    print(file_help.read())


server = Server()
server.start_manager()
