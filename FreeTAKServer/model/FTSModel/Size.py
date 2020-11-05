from FreeTAKServer.model.FTSModelVariables.SizeVariables import SizeVariables as vars

class Size:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        size = Size()

        size.setINTAG(INTAG)

        return size

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG