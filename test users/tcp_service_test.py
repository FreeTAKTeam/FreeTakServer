import unittest
from test import support
import socket
import test_cot_data
import time
from lxml import etree
import uuid

class TCPServiceTests(unittest.TestCase):
    def setUp(self):
        """ setup method to establish two sockets.

        this method is run prior to any other tests running and will create the basic sockets
        required for further testing.

        """
        self.client_socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def test_clientinformation_is_not_sent(self):
        """ this method tests that client data is not resent after disconnections

        test procedure:
        client A conn-> FTS
        client A clientinfo-> FTS
        client A close-> FTS

        client B conn-> FTS
        client B clientinfo-> FTS
        client B <-otherclientinfo FTS
        client B otherclientinfo != clientAinfo
        client B close-> FTS
        """

        client_a_object = self.connect_client_to_server(sock = self.client_socket_a, ip = '127.0.0.1', port = 15777, uid = '245397c8-69f7-4f68-979e-685ff7ee1451')  # establish client A connection
        time.sleep(1)
        self.client_socket_a.close()

        time.sleep(5)  # if this delay is reduced the test fails as FTS doesn't have time to process the changes
        client_b_object = self.connect_client_to_server(sock = self.client_socket_b, ip = '127.0.0.1', port = 15777)  # establish client B connection
        time.sleep(1)
        # receive data and assert client_a_data not in resent data
        start = time.time()
        delay = 3  # 10 second delay
        while time.time() < start+delay:
            data = b''
            self.client_socket_b.settimeout(0.1)
            while b'</event>' not in data:
                try:
                    data += self.client_socket_b.recv(1)
                except socket.timeout:
                    break
            if data == b'':
                break
            cot = etree.fromstring(data)
            self.assertNotEqual(client_a_object.uid, cot.get('uid'))

        self.client_socket_b.close()  # disconnect final socket

    def connect_client_to_server(self, sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM), ip: str = '127.0.0.1', port: int = 15777, uid: str = str(uuid.uuid4())) -> test_cot_data.TestCoTClient:
        """this method is used to connect a client to the server and send a basic connection message
        """
        sock.connect((ip, port))
        client_object = test_cot_data.TestCoTClient(uid=uid)
        sock.send(client_object.generate_cot())
        return client_object


if __name__ == '__main__':
    unittest.main()
