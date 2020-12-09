from FreeTAKServer.model.FTSModelVariables.KeywordsVariables import KeywordsVariables as vars

class Keywords:
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def CreateExCheckTemplate(INTAG=vars.CreateExCheckTemplate().INTAG, ):
        keywords = Keywords()

        keywords.setINTAG(INTAG)

        return keywords

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
