from .FederationServerServiceVariables import FederationServerServiceVariables as vars


class FederationServerService:
    def __init__(self, FederationServerServiceIP=vars().FederationServerServiceIP,
                 FederationServerServicePort=vars().FederationServerServicePort,
                 FederationServerServiceStatus=vars().FederationServerServiceStatus):
        self.FederationServerServiceIP = FederationServerServiceIP
        self.FederationServerServicePort = FederationServerServicePort
        self.FederationServerServiceStatus = FederationServerServiceStatus
