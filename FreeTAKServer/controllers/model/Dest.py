
class Dest:
    def __init__(self, xml):
        self.callsign = None
        self.setcallsign(xml.get('callsign'))

    def getcallsign(self):
        return self.callsign

    def setcallsign(self, callsign=0):
        self.callsign = self.callsign
