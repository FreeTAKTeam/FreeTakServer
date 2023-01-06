from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables._GroupVariables import _GroupVariables as vars
class _Group(FTSProtocolObject):
    def __init__(self):
        self.name = None
        self.role = None

    def getrole(self):
        return self.role

    def setrole(self, role):
        self.role = role

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name
