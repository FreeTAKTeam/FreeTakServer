from FreeTAKServer.model.SpecificCoT.SendHealthCheck import SendHealthCheck


class SendHealthCheckController:
    # TODO: deprecate this function
    def __init__(self, RawCoT):
        self.RawCoT = RawCoT
        self.HealthCheck = SendHealthCheck()
        self.HealthCheck.xmlString = RawCoT.xmlString
        self.HealthCheck.clientInformation = RawCoT.clientInformation

    def getObject(self):
        return self.HealthCheck
