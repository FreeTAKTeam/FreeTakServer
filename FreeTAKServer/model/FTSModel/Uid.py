from FreeTAKServer.model.FTSModelVariables.UidVariables import UidVariables as vars

class Uid:
    def __init__(self):
        self.Droid = None

    @staticmethod
    def connection(DROID = vars.connection().DROID):
        uid = Uid()
        uid.setDroid(DROID)
        return uid

    @staticmethod
    def UserUpdate(DROID=vars.UserUpdate().Droid):
        uid = Uid()
        uid.setDroid(DROID)
        return uid

    @staticmethod
    def CreateExCheckTemplate(INTAG = vars.CreateExCheckTemplate().INTAG):
        uid = Uid()
        uid.setINTAG(INTAG)
        return uid

    def getDroid(self):
        return self.Droid

    def setDroid(self, Droid = None):
        self.Droid = Droid

    def getINTAG(self):
        return self.INTAG

    def setINTAG(self, INTAG = None):
        self.INTAG = INTAG

