from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

class DataPackageServiceVariables:
    def __init__(self):
        self.DataPackageServiceIP = MainConfig.DataPackageServiceDefaultIP
        self.DataPackageServicePort = 8080
        self.DataPackageServiceStatus = ""