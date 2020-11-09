from FreeTAKServer.model.FTSModelVariables.TimestampVariables import TimestampVariables as vars

class Timestamp:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        timestamp = Timestamp()

        timestamp.setINTAG(INTAG)

        return timestamp

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG