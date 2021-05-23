from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.ConnectionEntry import ConnectionEntry

class _Video(FTSProtocolObject):
    def __init__(self):
        pass

    @staticmethod
    def VideoStream():
        _video = _Video()
        _video.ConnectionEntry = ConnectionEntry.VideoStream()
        return _video

    def getConnectionEntry(self):
        return self.ConnectionEntry

    def setConnectionEntry(self, ConnectionEntry):
        self.ConnectionEntry = ConnectionEntry