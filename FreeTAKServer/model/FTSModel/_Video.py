from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModel.ConnectionEntry import ConnectionEntry
from FreeTAKServer.model.FTSModelVariables._VideoVariables import _Video as vars

class _Video(FTSProtocolObject):
    def __init__(self):
        self.sensor = None
        self.spi = None
        self.url = None

    @staticmethod
    def VideoStream():
        _video = _Video()
        _video.ConnectionEntry = ConnectionEntry.VideoStream()
        return _video

    @staticmethod
    def DroneSensor(SENSOR=vars.DroneSensor().sensor, SPI=vars.DroneSensor().spi, URL=vars.DroneSensor().url, ):
        _video = _Video()
        _video.setsensor(SENSOR)
        _video.setspi(SPI)
        _video.seturl(URL)

        return _video

    @staticmethod
    def BitsImageryVideo():
        _video = _Video()
        _video.ConnectionEntry = ConnectionEntry.BitsImageryVideo()
        return _video

    def getConnectionEntry(self):
        return self.ConnectionEntry

    def setConnectionEntry(self, ConnectionEntry):
        self.ConnectionEntry = ConnectionEntry

    def getsensor(self):
            return self.sensor

    def setsensor(self, sensor):
        self.sensor = sensor

    def getspi(self):
            return self.spi

    def setspi(self, spi):
        self.spi = spi

    def geturl(self):
            return self.url

    def seturl(self, url):
        self.url = url