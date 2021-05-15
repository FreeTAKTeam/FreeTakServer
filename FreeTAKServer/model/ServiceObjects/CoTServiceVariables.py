from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

class CoTServiceVariables:
    def __init__(self):
        self.CoTServiceIP = "0.0.0.0"
        self.CoTServicePort = MainConfig.CoTServicePort
        self.CoTServiceStatus = ""