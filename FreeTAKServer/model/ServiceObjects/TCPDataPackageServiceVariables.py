from FreeTAKServer.controllers.configuration.MainConfig import MainConfig


class TCPDataPackageServiceVariables:
    def __init__(self):
        self.TCPDataPackageServiceIP = MainConfig.DataPackageServiceDefaultIP
        self.TCPDataPackageServicePort = 8080
        self.TCPDataPackageServiceStatus = ""
