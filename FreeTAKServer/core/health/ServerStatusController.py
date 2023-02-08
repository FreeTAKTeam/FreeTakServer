import socket

import requests
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.connection.SSLSocketController import SSLSocketController
from FreeTAKServer.model.ServiceObjects.FTS import FTS

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

def modifyDefaultIP(func):
    def changeDefaultIP(instance, port, ip):
        import socket
        if ip == "0.0.0.0":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
            ip = IP
            func(instance, port, ip)
        else:
            func(instance, port, ip)
    return changeDefaultIP

class ServerStatusController:

    def __init__(self, ServerStatusObject: FTS):
        mapping = {"start": "on", "stop": "off", "": ""}
        self.TCPCoTStatus = self.TCPCoTStatusCheck(ServerStatusObject.CoTService.CoTServicePort, ServerStatusObject.CoTService.CoTServiceIP)
        self.TCPCoTStatusExpected = mapping[ServerStatusObject.CoTService.CoTServiceStatus]

        self.TCPDataPackageStatus = self.TCPDataPackageStatusCheck(ServerStatusObject.TCPDataPackageService.TCPDataPackageServicePort, ServerStatusObject.TCPDataPackageService.TCPDataPackageServiceIP)
        self.TCPDataPackageStatusExpected = mapping[ServerStatusObject.TCPDataPackageService.TCPDataPackageServiceStatus]

        self.SSLCoTStatus = self.SSLCoTStatusCheck(ServerStatusObject.SSLCoTService.SSLCoTServicePort, ServerStatusObject.SSLCoTService.SSLCoTServiceIP)
        self.SSLCoTStatusExpected = mapping[ServerStatusObject.SSLCoTService.SSLCoTServiceStatus]

        self.SSLDataPackageStatus = self.SSLDataPackageStatusCheck(ServerStatusObject.SSLDataPackageService.SSLDataPackageServicePort, ServerStatusObject.SSLDataPackageService.SSLDataPackageServiceIP)
        self.SSLDataPackageStatusExpected = mapping[ServerStatusObject.SSLDataPackageService.SSLDataPackageServiceStatus]

        self.RestAPIStatus = self.RestAPIStatusCheck(ServerStatusObject.RestAPIService.RestAPIServicePort, ServerStatusObject.RestAPIService.RestAPIServiceIP)
        self.RestAPIStatusExpected = mapping[ServerStatusObject.RestAPIService.RestAPIServiceStatus]

        self.FederationServerStatus = self.FederationServerStatusCheck(ServerStatusObject.FederationServerService.FederationServerServicePort, ServerStatusObject.FederationServerService.FederationServerServiceIP)
        self.FederationServerExpected = mapping[ServerStatusObject.FederationServerService.FederationServerServiceStatus]

    def FederationServerStatusCheck(self, FederationPort, IP):
        try:
            if IP == "0.0.0.0":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            else:
                pass
            sock = SSLSocketController().createClientSocket(IP)
            sock.settimeout(5)
            sock.connect((IP, FederationPort))
            # returnMessage = sock.recv(100)
            sock.close()
            return "on"
        except Exception as e:
            print('here')
            print(e)
            return "off"

    def TCPDataPackageStatusCheck(self, TCPDataPackagePort, IP):
        try:
            if IP == "0.0.0.0":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            else:
                pass
            conn = requests.get(f'http://{IP}:{TCPDataPackagePort}/Alive')
            if conn.status_code == 200:
                return "on"
            else:
                return "off"
        except Exception as e:
            return "off"

    def TCPCoTStatusCheck(self, TCPCoTPort, IP):
        try:
            if IP == "0.0.0.0":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            else:
                pass
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, TCPCoTPort))
            sock.send(b'TEST')
            returnMessage = sock.recv(100)
            sock.close()

            if returnMessage == b'success':
                return "on"
            else:
                return "off"
        except Exception as e:
            return "off"

    def SSLDataPackageStatusCheck(self, SSLDataPackagePort, IP):
        try:
            if IP == "0.0.0.0":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            else:
                pass
            conn = requests.get(f'https://{IP}:{SSLDataPackagePort}/Alive', cert=(config.pemDir, config.unencryptedKey), verify=False)
            if conn.status_code == 200:
                return "on"
            else:
                return "off"
        except:
            return "off"

    def SSLCoTStatusCheck(self, SSLCoTPort, IP):
        try:
            import socket
            if IP == "0.0.0.0":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            else:
                pass
            sock = SSLSocketController().createClientSocket(IP)
            sock.settimeout(10)
            sock.connect((IP, SSLCoTPort))
            sock.send(b'success')
            returnMessage = sock.recv(100)
            sock.close()
            if returnMessage == b'success':
                return "on"
            else:
                return "off"
        except Exception as e:
            return "off"

    def RestAPIStatusCheck(self, RestAPIPort, IP):
        from eventlet.green.urllib import request
        try:
            import socket
            if IP == "0.0.0.0":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('10.255.255.255', 1))
                IP = s.getsockname()[0]
            else:
                pass
            conn = request.urlopen(f'http://{IP}:{RestAPIPort}/Alive')  # pylint: disable=no-member
            # request does have this method
            if conn.code == 200:
                return "on"
            else:
                return "off"
        except:
            return "off"


if __name__ == '__main__':
    status = ServerStatusController(FTS())
