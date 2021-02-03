from .FederationClientServiceVariables import FederationClientServiceVariables as vars


class FederationClientService:
    def __init__(self, FederationClientServiceIP=vars().FederationClientServiceIP,
                 FederationClientServicePort=vars().FederationClientServicePort,
                 FederationClientServiceStatus=vars().FederationClientServiceStatus):
        self.FederationClientServiceIP = FederationClientServiceIP
        self.FederationClientServicePort = FederationClientServicePort
        self.FederationClientServiceStatus = FederationClientServiceStatus
