from Model.dest import dest

class marti:
    def getdestcallsign(self):
        return dest.getcallsign()
    
    def setdestcallsign(self, callsign = 0):
        return dest.setcallsign(callsign)