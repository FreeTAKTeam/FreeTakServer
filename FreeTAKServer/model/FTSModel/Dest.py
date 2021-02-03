from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.DestVariables import DestVariables as vars


class Dest(FTSProtocolObject):
    def __init__(self, CALLSIGN=vars.other().CALLSIGN):
        self.callsign = None
        self.__settercalled = False
        self.__gettercalled = False
        # self.setcallsign(CALLSIGN)

    @staticmethod
    def other(CALLSIGN=vars.geochat().CALLSIGN):
        dest = Dest()

        return dest

    @staticmethod
    def geochat(CALLSIGN=vars.geochat().CALLSIGN):
        dest = Dest()
        # dest.setcallsign(CALLSIGN)
        return dest

    def getcallsign(self):
        self.__gettercalled = True
        return self.callsign

    def setcallsign(self, callsign=0):
        self.callsign = callsign
        self.__settercalled = True

    def _settercalled(self):
        return self.__settercalled

    def _gettercalled(self):
        return self.__gettercalled
