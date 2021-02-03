from .SSLCoTServiceVariables import SSLCoTServiceVariables as vars


class SSLCoTService:
    def __init__(self, CoTServiceIP=vars().SSLCoTServiceIP,
                 CoTServicePort=vars().SSLCoTServicePort,
                 CoTServiceStatus=vars().SSLCoTServiceStatus):
        self.SSLCoTServiceIP = CoTServiceIP
        self.SSLCoTServicePort = CoTServicePort
        self.SSLCoTServiceStatus = CoTServiceStatus
