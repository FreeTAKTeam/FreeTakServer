from FreeTAKServer.controllers.model.SendHealthCheck import SendHealthCheck

class SendHealthCheckController:
    def __init__(self, RawCoT):
        self.RawCoT = RawCoT
        self.m_HealthCheck = SendHealthCheck()
        self.m_HealthCheck.xmlString = RawCoT.xmlString
        self.m_HealthCheck.clientInformation = RawCoT.clientInformation

    def getObject(self):
        return self.m_HealthCheck