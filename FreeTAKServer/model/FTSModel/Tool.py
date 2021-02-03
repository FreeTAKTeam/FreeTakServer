from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.ToolVariables import ToolVariables as vars


class Tool(FTSProtocolObject):
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG, ):
        tool = Tool()

        tool.setINTAG(INTAG)

        return tool

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
