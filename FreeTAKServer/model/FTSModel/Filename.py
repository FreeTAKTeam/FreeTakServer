from FreeTAKServer.model.FTSModelVariables.FilenameVariables import FilenameVariables as vars

class Filename:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        filename = Filename()

        filename.setINTAG(INTAG)

        return filename

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG