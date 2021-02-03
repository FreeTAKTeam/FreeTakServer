from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.DescriptionVariables import DescriptionVariables as vars


class Description(FTSProtocolObject):
    @staticmethod
    def Checklist(INTAG=vars.Checklist().INTAG):
        description = Description()
        description.setINTAG(INTAG)
        return description

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
