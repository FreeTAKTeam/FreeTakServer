from FreeTAKServer.model.FTSModelVariables.CreatorUidVariables import CreatorUidVariables as vars

class CreatorUid:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        creatoruid = CreatorUid()

        creatoruid.setINTAG(INTAG)

        return creatoruid

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG