from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables._uastoolVariables import _uastoolVariables as vars

class _Uastool(FTSProtocolObject):
    def __init__(self):
        self.extendedCot = None
        self.activeRoute = None

 
    def getextendedCot(self):
            return self.extendedCot

    def setextendedCot(self, extendedCot):
        self.extendedCot = extendedCot

    def getactiveRoute(self):
            return self.activeRoute

    def setactiveRoute(self, activeRoute):
        self.activeRoute = activeRoute