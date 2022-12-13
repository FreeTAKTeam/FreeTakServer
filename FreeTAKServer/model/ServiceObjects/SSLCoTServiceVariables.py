from FreeTAKServer.core.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class SSLCoTServiceVariables:
    def __init__(self):
        self.SSLCoTServiceIP = "0.0.0.0"
        self.SSLCoTServicePort = config.SSLCoTServicePort
        self.SSLCoTServiceStatus = ""