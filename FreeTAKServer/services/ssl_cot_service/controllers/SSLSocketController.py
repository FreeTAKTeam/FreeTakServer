from FreeTAKServer.core.connection.MainSocketController import MainSocketController
from FreeTAKServer.model.sockets.SSLServerSocket import SSLServerSocket
import ssl
import socket
import OpenSSL


class SSLSocketController(MainSocketController):
    def __init__(self):
        self.MainSocket = SSLServerSocket()
        
    def get_context(self, protocol):
        context = ssl.SSLContext(protocol=protocol)
        context.load_verify_locations(cafile=self.MainSocket.CA)
        context.load_verify_locations(cafile=self.MainSocket.CRLFile)
        
        return context
        
    def createSocket(self):
        context = self.get_context(ssl.PROTOCOL_TLS_SERVER)
        context.verify_mode = ssl.CERT_REQUIRED
        context.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
        context.load_cert_chain(certfile=self.MainSocket.pemDir, keyfile=self.MainSocket.keyDir,
                                password=self.MainSocket.password, )
        self.MainSocket.sock = socket.socket(self.MainSocket.socketAF, self.MainSocket.socketSTREAM)
        self.MainSocket.sock.setsockopt(self.MainSocket.solSock, self.MainSocket.soReuseAddr,
                                        self.MainSocket.sockProto)
        self.MainSocket.sock.bind((self.MainSocket.ip, self.MainSocket.port))
        #self.MainSocket.sock = context.wrap_socket(self.MainSocket.sock, server_side=True)
        return self.MainSocket.sock
        
    def wrap_client_socket(self, socket):
        context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
        context.load_verify_locations(cafile=self.MainSocket.CA)
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_SSLv2
        context.verify_mode = ssl.CERT_REQUIRED
        context.verify_flags = ssl.VERIFY_CRL_CHECK_LEAF
        context.load_cert_chain(certfile=self.MainSocket.pemDir, keyfile=self.MainSocket.keyDir,
                                password=self.MainSocket.password, )
        sock = context.wrap_socket(socket, server_side=True)
        return sock

    def createClientSocket(self, serverIP):
        context = ssl.SSLContext()
        context.load_verify_locations(cafile=self.MainSocket.CA)
        context.load_cert_chain(certfile=self.MainSocket.pemDir, keyfile=self.MainSocket.keyDir,
                                password=self.MainSocket.password, )
        context.verify_mode = ssl.CERT_OPTIONAL
        context.check_hostname = False
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        self.MainSocket.sock = socket.socket(self.MainSocket.socketAF, self.MainSocket.socketSTREAM)
        # self.MainSocket.sock = context.wrap_socket(self.MainSocket.sock)
        return self.MainSocket.sock