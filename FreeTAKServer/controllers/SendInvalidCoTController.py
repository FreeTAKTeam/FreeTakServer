from FreeTAKServer.controllers.model.SendInvalidCoT import SendInvalidCoT
class SendInvalidCoTController:
    def __init__(self, RawCOT):
        self.SendInvalidCoT = SendInvalidCoT()
        self.SendInvalidCoT.clientInformation = RawCOT.clientInformation

    def getObject(self):
        return self.SendInvalidCoT