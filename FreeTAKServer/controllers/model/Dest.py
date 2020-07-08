
class Dest:
    def __init__(self, xml):
        self.callsign = None
        try:
            self.setcallsign(xml.get('callsign'))
        except Exception as e:
            pass

    def getcallsign(self):
        return self.callsign

    def setcallsign(self, callsign=0):
        self.callsign = callsign
