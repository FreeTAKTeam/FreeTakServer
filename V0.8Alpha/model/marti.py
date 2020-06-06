from .dest import dest

class marti:
    def __init__(self):
        self.m_dest = dest()

    def getdestcallsign(self):
        return self.m_dest.getcallsign()
    
    def setdestcallsign(self, callsign = 0):
        return self.m_dest.setcallsign(callsign)