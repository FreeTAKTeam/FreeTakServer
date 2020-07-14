from .Dest import Dest
from .DestList import DestList

class Marti:
    def __init__(self, xml):
        destList = xml.findall('dest')
        for dest in destList:
            self.m_Dest = Dest(dest)

        self.m_DestList = DestList.setDestList(destList)

    def getDestcallsign(self):
        return self.m_Dest.getcallsign()
    
    def setDestcallsign(self, callsign = 0):
        return self.m_Dest.setcallsign(callsign)
