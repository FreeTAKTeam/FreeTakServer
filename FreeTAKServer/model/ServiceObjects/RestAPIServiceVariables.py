from FreeTAKServer.controllers.configuration.MainConfig import MainConfig


class RestAPIServiceVariables:
    def __init__(self):
        self.RestAPIServiceIP = MainConfig.APIIP
        self.RestAPIServicePort = MainConfig.APIPort
        self.RestAPIServiceStatus = ""
