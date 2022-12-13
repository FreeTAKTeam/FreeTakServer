from FreeTAKServer.core.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class CoTServiceVariables:
    def __init__(self):
        self.CoTServiceIP = "0.0.0.0"
        self.CoTServicePort = config.CoTServicePort
        self.CoTServiceStatus = ""