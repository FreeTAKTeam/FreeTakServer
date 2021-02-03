from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.Contact import Contact


class Group(FTSProtocolObject):
    def __init__(self, xml):
        self.uid = None
        self.name = None
        self.setuid(xml.get('uid'))
        self.setname(xml.get('name'))
        try:
            self.contact = Contact()
        except BaseException:
            pass
        try:
            self.Group = Group(xml.find('group'))
        except BaseException:
            pass

    def setuid(self, uid=None):
        self.uid = uid

    def getuid(self):
        return self.uid

    def setname(self, name=None):
        self.name = name

    def getname(self):
        return self.name
