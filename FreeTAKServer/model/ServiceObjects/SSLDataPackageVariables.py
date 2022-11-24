from FreeTAKServer.controllers.configuration.MainConfig import MainConfig

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

class SSLDataPackageVariables:
    def __init__(self):
        self.SSLDataPackageIP = config.DataPackageServiceDefaultIP
        self.SSLDataPackagePort = 8443
        self.SSLDataPackageStatus = ""