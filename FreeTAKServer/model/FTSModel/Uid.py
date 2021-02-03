from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.UidVariables import UidVariables as vars


class Uid(FTSProtocolObject):
    def __init__(self):
        self.Droid = None

    @staticmethod
    def connection(DROID=vars.connection().DROID):
        uid = Uid()
        uid.setDroid(DROID)
        return uid

    @staticmethod
    def UserUpdate(DROID=vars.UserUpdate().Droid):
        uid = Uid()
        uid.setDroid(DROID)
        return uid

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG):
        uid = Uid()
        uid.setINTAG(INTAG)
        return uid

    @staticmethod
    def Checklist(INTAG=vars.Checklist().INTAG):
        uid = Uid()
        uid.setINTAG(INTAG)
        return uid

    def getDroid(self):
        return self.Droid

    def setDroid(self, Droid=None):
        self.Droid = Droid

    def getINTAG(self):
        return self.INTAG

    def setINTAG(self, INTAG=None):
        self.INTAG = INTAG
