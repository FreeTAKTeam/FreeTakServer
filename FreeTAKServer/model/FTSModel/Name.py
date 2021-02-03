from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.NameVariables import NameVariables as vars


class Name(FTSProtocolObject):
    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG):
        name = Name()
        name.setINTAG(INTAG)
        return name

    @staticmethod
    def Checklist(INTAG=vars.Checklist().INTAG):
        name = Name()
        name.setINTAG(INTAG)
        return name

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
