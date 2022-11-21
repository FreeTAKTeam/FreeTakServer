from FreeTAKServer.model.sockets.MainSocket import MainSocket
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class SSLServerSocket(MainSocket):
    def __init__(self):
        super().__init__()
        self.keyDir = config.keyDir
        self.pemDir = config.pemDir
        self.testKeyDir = config.testKey
        self.testPemDir = config.testPem
        self.password = config.password
        self.CA = config.CA