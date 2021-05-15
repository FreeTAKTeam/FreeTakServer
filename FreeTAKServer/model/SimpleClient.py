from .SimpleClientVariables import SimpleClientVariables as vars

class SimpleClient:
    def __init__(self, IP = vars().IP, CALLSIGN = vars().CALLSIGN, TEAM = vars().TEAM):
        self.ip = IP
        self.callsign = CALLSIGN
        self.team = TEAM