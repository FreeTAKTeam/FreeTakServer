from .RestAPIServiceVariables import RestAPIServiceVariables as vars


class RestAPIService:
    def __init__(self, IP=vars().RestAPIServiceIP, Port=vars().RestAPIServicePort, Status=vars().RestAPIServiceStatus):
        self.RestAPIServiceIP = IP
        self.RestAPIServicePort = Port
        self.RestAPIServiceStatus = Status
