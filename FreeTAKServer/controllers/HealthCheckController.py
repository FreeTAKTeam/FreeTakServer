import socket
import time
# TODO: remove strings


class HealthCheckController:
    def __init__(self, port, ip):
        self.connectionString = b'<?xml version="1.0" encoding="UTF-8"?><event><detail><connection conn="True"/></detail></event>'
        self.dataString = b'<?xml version="1.0" encoding="UTF-8"?><event><detail><healthCheck healthy="True"/></detail></event>'
        self.ip = ip
        self.port = port
        self.health = []
        connection = self.establishConnection()
        if connection == 'connection successful':
            dataRecieved = self.receiveData()
            if dataRecieved:
                self.health = [1, 1]
            else:
                self.health = [1, 0]
        else:
            self.health = [0, 0]
        self.s.send(b'')

    def establishConnection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip, self.port))
        except BaseException:
            return 'connection failed'
        self.s.send(self.connectionString)
        self.s.recv(2048)
        return 'connection successful'

    def receiveData(self):
        try:
            timeout = 30
            time.sleep(2)
            self.s.send(self.dataString)
            timeout_start = time.time()
            foundData = False
            self.s.settimeout(10)
            while time.time() < timeout_start + timeout:
                data = self.s.recv(2048)
                if data == self.dataString:
                    foundData = True
                    break
                else:
                    pass
            return foundData
        except BaseException:
            return False
        self.s.send(b'')
        self.s.close()

    def returnHealth(self):
        return self.health
