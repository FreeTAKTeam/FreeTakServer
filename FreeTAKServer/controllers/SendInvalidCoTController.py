from FreeTAKServer.controllers.model.SendInvalidCoT import SendInvalidCoT
class SendInvalidCoTController:
    def __init__(self, RawCOT):
        self.m_SendInvalidCoT = SendInvalidCoT()
        self.m_SendInvalidCoT.clientInformation = RawCOT.clientInformation

    def getObject(self):
        return self.m_SendInvalidCoT