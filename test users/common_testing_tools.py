import socket
import time
import asyncio
import test_data
import ssl

class TCPClient:
    def __init__(self, ip, port):
        self.clientObj = test_data.TestCoTClient()
        self.sock = self.establish_socket_connection(ip=ip, port=port)

    def establish_socket_connection(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(self.clientObj.generate_cot())
        return sock

    def send_specific_data(self, cot: bytes):
        self.sock.send(cot)

    def service_connection(self):
        self.receive_data_until_empty()
        self.send_connection_data()

    def receive_data_until_empty(self):
        self.sock.settimeout(0.1)
        while True:
            try:
                self.sock.recv(100000)
            except:
                break

    def receive_specific_data(self, buffer: int):
        return self.sock.recv(buffer)

    def send_connection_data(self):
        self.sock.send(self.clientObj.generate_cot())
        self.sock.send(test_data.TestCoTClient().generate_object_cot())

    def connection_is_alive(self):
        try:
            self.sock.send(test_data.TestCoTClient().generate_object_cot())
            if self.sock.recv(5) != b'':
                return True
            else:
                return False
        except:
            return False

class TCPClientAsync:
    def __init__(self, ip, port):
        self.clientObj = test_data.TestCoTClient()
        self.sock = self.establish_socket_connection(ip=ip, port=port)

    def establish_socket_connection(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.send(self.clientObj.generate_cot())
        return sock

    async def service_connection(self):
        asyncio.create_task(self.receive_data_until_empty())
        asyncio.create_task(self.send_connection_data())

    async def receive_data_until_empty(self):
        self.sock.settimeout(0.1)
        while True:
            try:
                self.sock.recv(100000)
            except:
                break

    async def send_connection_data(self):
        self.sock.send(self.clientObj.generate_cot())
        self.sock.send(test_data.TestCoTClient().generate_object_cot())

    def connection_is_alive(self):
        try:
            self.sock.send(test_data.TestCoTClient().generate_object_cot())
            if self.sock.recv(5) != b'':
                return True
            else:
                return False
        except:
            return False

class SSLClientAsync:
    def __init__(self, cert_file, key_file, ip, port):
        self.clientObj = test_data.TestCoTClient()
        self.sock = self.establish_socket_connection(cert_file=cert_file, key_file=key_file, ip=ip, port=port)

    def establish_socket_connection(self, cert_file, key_file, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile=cert_file, keyfile=key_file)
        ssl_sock.connect((ip, port))
        ssl_sock.send(self.clientObj.generate_cot())
        return ssl_sock

    async def service_connection(self):
        self.send_connection_data()

    async def receive_data_until_empty(self):
        self.sock.settimeout(0.1)
        while True:
            try:
                self.sock.recv(100000)
            except:
                break

    def send_connection_data(self):
        self.sock.send(self.clientObj.generate_cot())
        self.sock.send(test_data.TestCoTClient().generate_object_cot())

    def connection_is_alive(self):
        try:
            self.sock.send(test_data.TestCoTClient().generate_object_cot())
            if self.sock.recv(5) != b'':
                return True
            else:
                return False
        except:
            return False