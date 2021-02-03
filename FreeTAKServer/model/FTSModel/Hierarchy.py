from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from .Group import Group


class Hierarchy(FTSProtocolObject):
    def __init__(self, xml):
        try:
            self.Group = Group(xml.find('group'))
        except BaseException:
            pass
