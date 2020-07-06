from .Dest import Dest

class Marti:
    def __init__(self):
        self.m_Dest = Dest()

    def getDestcallsign(self):
        return self.m_Dest.getcallsign()
    
    def setDestcallsign(self, callsign = 0):
        return self.m_Dest.setcallsign(callsign)
