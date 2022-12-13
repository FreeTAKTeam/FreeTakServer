from FreeTAKServer.core.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class FederationServerServiceVariables:
    def __init__(self):
        # TODO: change to default ''
        self.FederationServerServiceStatus = 'stop'
        self.FederationServerServicePort = config.FederationPort
        self.FederationServerServiceIP = "0.0.0.0"