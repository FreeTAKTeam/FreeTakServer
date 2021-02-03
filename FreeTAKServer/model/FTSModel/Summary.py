from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.SummaryVariables import SummaryVariables as vars


class Summary(FTSProtocolObject):
    def __init__(self):
        self.INTAG = vars().INTAG

    @staticmethod
    def drop_point(INTAG=vars.drop_point().INTAG):
        summary = Summary()
        summary.INTAG = INTAG
        return summary

    def setINTAG(self, INTAG=None):
        self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
