from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.CreatorUidVariables import CreatorUidVariables as vars


class CreatorUid(FTSProtocolObject):
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG, ):
        creatoruid = CreatorUid()

        creatoruid.setINTAG(INTAG)

        return creatoruid

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG

    @staticmethod
    def Checklist(INTAG=vars.Checklist().INTAG):
        creatorUid = CreatorUid()
        creatorUid.setINTAG(INTAG)
        return creatorUid
