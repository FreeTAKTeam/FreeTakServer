from .DestVariables import DestVariables as vars

class Dest:
    def __init__(self, CALLSIGN = vars.other().CALLSIGN):
        self.callsign = None
        self.setcallsign(CALLSIGN)

    @staticmethod
    def other(CALLSIGN = vars.geochat().CALLSIGN):
        dest = Dest()

        return dest

    @staticmethod
    def geochat(CALLSIGN = vars.geochat().CALLSIGN):
        dest = Dest()
        dest.setcallsign(CALLSIGN)
        return dest

    def getcallsign(self):
        return self.callsign

    def setcallsign(self, callsign=0):
        self.callsign = callsign
