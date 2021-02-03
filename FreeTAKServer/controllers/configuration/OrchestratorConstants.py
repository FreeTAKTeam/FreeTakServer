
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig


class OrchestratorConstants:
    def __init__(self):
        self.CoTIP = "0.0.0.0"
        self.COTPORT = MainConfig.CoTServicePort
        self.APIPORTARG = '-APIPort'
        self.COTPORTARG = '-CoTPort'
        self.IPARG = "-IP"
        self.APIPORTDESC = 'the port address you would like FreeTAKServer to run receive datapackages on not'
        self.IPDESC = "the IP you would like FreeTAKServer to run receive connections on, must be set for private DataPackages to function"
        self.COTPORTDESC = 'the port you would like FreeTAKServer to run receive connections on'
        self.COTIPDESC = 'the IP you would like FreeTAKServer to run receive connections on'
        self.SSLCOTPORTDESC = 'the port you would like FreeTAKServer to run receive SSL connections on'
        self.SSLCOTIPDESC = 'the IP you would like FreeTAKServer to run receive SSL connections on'
        self.FULLDESC = 'FreeTAKServer startup settings'
        self.HEALTHCHECK = 'HealthCheck'
        self.LOCALHOST = '127.0.0.1'

        self.DEFAULTCONNECTIONGEOCHATOBJ = MainConfig.ConnectionMessage
