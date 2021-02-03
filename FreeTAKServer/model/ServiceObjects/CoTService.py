from .CoTServiceVariables import CoTServiceVariables as vars


class CoTService:
    def __init__(self, CoTServiceIP=vars().CoTServiceIP,
                 CoTServicePort=vars().CoTServicePort,
                 CoTServiceStatus=vars().CoTServiceStatus):
        self.CoTServiceIP = CoTServiceIP
        self.CoTServicePort = CoTServicePort
        self.CoTServiceStatus = CoTServiceStatus
