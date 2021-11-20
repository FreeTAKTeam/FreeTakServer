import unittest
import socket
import ssl
import time
import random
import threading
import uuid
import multiprocessing
import asyncio

from lxml import etree

import test_cot_data





def open_ssl_connection(cert_file, key_file, ip, port, test_client):
    """
    this function opens an ssl connection with TLSv1_2 and returns the open connection
    Args:
        test_client:
        ip:
        port:
        cert_file: the file containing the public certificate
        key_file: the file containing the private certificate
    Returns:
        ssl_sock: an open ssl connection
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile=cert_file, keyfile=key_file)
    ssl_sock.connect((ip, port))
    ssl_sock.send(test_client.generate_cot())
    return ssl_sock


def empty_buffer(ssl_sock):
    ssl_sock.settimeout(2)
    data = b'123'
    while data:
        try:
            data = ssl_sock.recv(1000000000)
        except:
            return None


def receive_data(ssl_sock):
    data = b''
    ssl_sock.settimeout(2)
    while b'</event>' not in data:
        try:
            data += ssl_sock.recv(1)
            if data:
                pass
            else:
                break
        except socket.timeout:
            break
    return data


class SSLServiceTest(unittest.TestCase):
    def setUp(self):
        self.ip = '192.168.2.129'
        self.port = 8089
        self.certfile = r'C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\certs\Client.pem'
        self.keyfile = r'C:\Users\natha\PycharmProjects\FreeTakServer\FreeTAKServer\certs\Client.key'

    def test_connection(self, certfile=None, keyfile=None):
        """
        this tests validates that the ssl socket is accepting connections
        Args:
            certfile: the file containing the public certificate
            keyfile: the file containing the private certificate
        """
        if certfile is None:
            certfile = self.certfile

        if keyfile is None:
            keyfile = self.keyfile

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile=certfile, keyfile=keyfile)
        ssl_sock.connect((self.ip, self.port))
        client_object = test_cot_data.TestCoTClient()
        ssl_sock.send(client_object.generate_cot())
        time.sleep(1)
        self.assertTrue(ssl_sock.recv(10000))
        ssl_sock.close()

    def test_send_ssl_data(self):
        print('test two')
        client_object_a = test_cot_data.TestCoTClient()
        ssl_sock_a = open_ssl_connection(ip=self.ip, port=self.port, cert_file=self.certfile, key_file=self.keyfile,
                                         test_client=client_object_a)

        # receive connection data
        start = time.time()
        while time.time() < start + 1:
            receive_data(ssl_sock=ssl_sock_a)

        client_object_b = test_cot_data.TestCoTClient()
        ssl_sock_b = open_ssl_connection(ip=self.ip, port=self.port, cert_file=self.certfile, key_file=self.keyfile,
                                         test_client=client_object_b)

        # receive connection data
        empty_buffer(ssl_sock=ssl_sock_b)

        test_object = test_cot_data.TestCoTClient()
        ssl_sock_a.send(test_object.generate_object_cot())
        time.sleep(1)
        data = receive_data(ssl_sock=ssl_sock_b)
        self.assertFalse(data == b"")
        cot = etree.fromstring(data)
        self.assertEqual(test_object.uid, cot.get('uid'))

        ssl_sock_a.close()
        ssl_sock_b.close()

    def high_volume_client_data_processing(self, number_of_client=20, test_length=5, maximum_time_delta=5):
        """ test to validate the maximum amount of data which a given instance of fts can process, implementing the delay
        as the determining factor.

        Args:
            number_of_client: number of clients which will be generated
            test_length: length of time in seconds for the test to run
            maximum_time_delta: maximum length of time between sending and receiving data from server

        """

        def data_sender():
            clients = {}
            for _ in range(number_of_client):
                # for _ in range(random.randint(1, 10)):
                client_object = test_cot_data.TestCoTClient()
                client = open_ssl_connection(ip=self.ip, port=self.port, cert_file=self.certfile, key_file=self.keyfile,
                                             test_client=client_object)
                clients[client_object.uid] = client

            nested_start = time.time()
            while time.time() < nested_start + test_length:
                uid = random.choice(list(clients.keys()))
                ssl_sock = clients[uid]
                ssl_sock.send(test_cot_data.TestCoTClient(uid=uid, callsign=str(uuid.uuid4())).generate_cot())
                receive_data(ssl_sock=ssl_sock)

        def data_receiver():
            pass

    def maintain_ssl_connection(self):
        long_running_client_object = test_cot_data.TestCoTClient()
        ssl_sock_long_running = open_ssl_connection(ip=self.ip, port=self.port, cert_file=self.certfile,
                                                    key_file=self.keyfile, test_client=long_running_client_object)

        # receive connection data
        start = time.time()
        while time.time() < start + 1:
            receive_data(ssl_sock=ssl_sock_long_running)

        def maintain_long_running_client():
            start = time.time()
            while time.time() < start + 360:
                ssl_sock_long_running.send(test_cot_data.TestCoTClient(uid=long_running_client_object.uid,
                                                                       callsign=str(uuid.uuid4())).generate_cot())
                time.sleep(random.randint(0, 1000) / 1000)
                start = time.time()
                while time.time() < start + random.randint(0, 1000) / 1000:
                    receive_data(ssl_sock=ssl_sock_long_running)

        def maintain_temp_clients():
            start = time.time()
            while time.time() < start + 360:
                clients = {}
                for _ in range(2):
                    # for _ in range(random.randint(1, 10)):
                    client_object = test_cot_data.TestCoTClient()
                    client = open_ssl_connection(ip=self.ip, port=self.port, cert_file=self.certfile,
                                                 key_file=self.keyfile, test_client=client_object)
                    clients[client_object.uid] = client

                nested_start = time.time()
                while time.time() < nested_start + 60:
                    uid = random.choice(list(clients.keys()))
                    ssl_sock = clients[uid]
                    ssl_sock.send(test_cot_data.TestCoTClient(uid=uid, callsign=str(uuid.uuid4())).generate_cot())
                    receive_data(ssl_sock=ssl_sock_long_running)

                for client in clients.values():
                    client.close()

        long_run = threading.Thread(target=maintain_long_running_client)
        temps = threading.Thread(target=maintain_temp_clients)
        long_run.start()
        temps.start()
        time.sleep(362)
        self.assertIsNone(ssl_sock_long_running.sendall(test_cot_data.TestCoTClient().generate_object_cot()))

    def test_ssl_client_disconnect_bug(self):
        from tcp_service_test import TCPClient
        """
        this method will attempt to trigger the SSL disconnect bug wherein the server will connect and
        then disconnect SSL clients continuously.

        """
        loop = asyncio.get_event_loop()
        tcp_clients = []
        ssl_clients = []
        for _ in range(20):
            ssl_clients.append(SSLClient(ip=self.ip, port=self.port, cert_file=self.certfile, key_file=self.keyfile))

        for _ in range(20):
            tcp_clients.append(TCPClient(ip=self.ip, port=8087))

        def call_ssl_client_service():
            start_time = time.time()
            nonlocal ssl_clients

            while time.time() < start_time + 10:
                for client in ssl_clients:
                    asyncio.create_task(client.service_connection())
                    time.sleep(1)

        def call_tcp_client_service():
            start_time = time.time()
            nonlocal tcp_clients

            while time.time() < start_time + 10:
                for client in tcp_clients:
                    asyncio.create_task(client.service_connection())
                    time.sleep(1)

        async def orchestrate():
            tcp_pool = multiprocessing.Pool(5)
            tcp_pool_procs = []
            ssl_pool = multiprocessing.Pool(5)
            ssl_pool_procs = []
            for _ in range(5):
                ssl_pool_procs.append(ssl_pool.apply_async(call_ssl_client_service, args=()))
                tcp_pool_procs.append(tcp_pool.apply_async(call_tcp_client_service, args=()))
            for proc in ssl_pool_procs:
                try:
                    proc.get()
                except:
                    pass
            for proc in tcp_pool_procs:
                try:
                    proc.get()
                except:
                    pass

        loop.run_until_complete(orchestrate())
        live_clients = 0
        dead_clients = 0
        for client in tcp_clients:
            if client.connection_is_alive():
                live_clients += 1
            else:
                dead_clients += 1

        for client in ssl_clients:
            if client.connection_is_alive():
                live_clients += 1
            else:
                dead_clients += 1

        print('number of live clients: ' + str(live_clients))
        print('number of dead clients: ' + str(dead_clients))
        self.assertTrue(live_clients == 40)

    def test_long_running_client(self):
        loop = asyncio.new_event_loop()
        client = SSLClient(ip=self.ip, port=self.port, cert_file=self.certfile, key_file=self.keyfile)
        start = time.time()
        while time.time()<start+10:
            loop.create_task(client.service_connection())
            time.sleep(1)
        self.assertTrue(client.connection_is_alive())

        

if __name__ == '__main__':
    unittest.main()
