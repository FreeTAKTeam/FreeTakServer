from FreeTAKServer.controllers.configuration.MainConfig import MainConfig


class SSLCoTServiceVariables:
    def __init__(self):
        self.SSLCoTServiceIP = "0.0.0.0"
        self.SSLCoTServicePort = MainConfig.SSLCoTServicePort
        self.SSLCoTServiceStatus = ""
