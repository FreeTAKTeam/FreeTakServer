from FreeTAKServer.model.FTSModelVariables.ToolVariables import ToolVariables as vars

class Tool:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        tool = Tool()

        tool.setINTAG(INTAG)

        return tool

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG