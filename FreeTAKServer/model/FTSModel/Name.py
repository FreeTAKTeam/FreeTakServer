from FreeTAKServer.model.FTSModelVariables.NameVariables import NameVariables as vars
class Name:
    @staticmethod
    def CreateExCheckTemplate(INTAG = vars.CreateExCheckTemplate().INTAG):
        name = Name()
        name.setINTAG(INTAG)
        return name

    def setINTAG(self, INTAG):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG