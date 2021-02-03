from FreeTAKServer.controllers.MainSocketController import MainSocketController
import socket


class TCPSocketController(MainSocketController):
    def createSocket(self):
        self.MainSocket.sock = socket.socket(self.MainSocket.socketAF, self.MainSocket.socketSTREAM)
        self.MainSocket.sock.setsockopt(self.MainSocket.solSock, self.MainSocket.soReuseAddr, self.MainSocket.sockProto)
        self.MainSocket.sock.bind((self.MainSocket.ip, self.MainSocket.port))
        return self.MainSocket.sock
