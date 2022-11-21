from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class RestAPIServiceVariables:
    def __init__(self):
        self.RestAPIServiceIP = config.APIIP
        self.RestAPIServicePort = config.APIPort
        self.RestAPIServiceStatus = ""