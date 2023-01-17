from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables._GroupVariables import _GroupVariables as vars
class _Group(FTSProtocolObject):
    def __init__(self):
        self.name = None
        self.role = None
        
    @staticmethod
    def connection(NAME = vars.connection().NAME, ROLE = vars.connection().ROLE):
        _group = _Group()
        _group.setname(NAME)
        _group.setrole(ROLE)
        return _group

    @staticmethod
    def UserUpdate(NAME=vars.UserUpdate().name, ROLE=vars.UserUpdate().role):
        _group = _Group()
        _group.setname(NAME)
        _group.setrole(ROLE)
        return _group

    @staticmethod
    def Presence(NAME=vars.Presence().name, ROLE=vars.Presence().role):
        _group = _Group()
        _group.setname(NAME)
        _group.setrole(ROLE)
        return _group
    
    def getrole(self):
        return self.role

    def setrole(self, role):
        self.role = role

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name