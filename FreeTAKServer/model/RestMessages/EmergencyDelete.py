from FreeTAKServer.model.RestMessages.Emergency import Emergency


class EmergencyDelete(Emergency):
    def __init__(self):
        pass

    def setuid(self, uid):
        self.uid = uid

    def getuid(self):
        return self.uid
