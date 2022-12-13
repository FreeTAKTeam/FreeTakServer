from FreeTAKServer.core.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class TCPDataPackageServiceVariables:
    def __init__(self):
        self.TCPDataPackageServiceIP = config.DataPackageServiceDefaultIP
        self.TCPDataPackageServicePort = 8080
        self.TCPDataPackageServiceStatus = ""