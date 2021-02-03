from FreeTAKServer.model.sockets.MainSocket import MainSocket
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig


class SSLServerSocket(MainSocket):
    def __init__(self):
        super().__init__()
        self.keyDir = MainConfig.keyDir
        self.pemDir = MainConfig.pemDir
        self.password = MainConfig.password
        self.CA = MainConfig.CA
