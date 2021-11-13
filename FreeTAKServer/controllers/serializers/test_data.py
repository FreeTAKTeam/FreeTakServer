from FreeTAKServer.model.FTSModel.Event import Event

from uuid import uuid4

class TestData:
    """
    this class contains the methods to create model objects of any CoT
    """
    def __init__(self):
        # dynamically create array of instantiated model objects
        self.test_data_arr = [getattr(self, func)() for func in dir(self) if callable(getattr(self, func)) and func[:2] != "__"]

    def SimpleCoT(self):
        """
        this method generates a GeoObject CoT

        """

        cot = Event.SimpleCoT()

        cot.setuid(str(uuid4()))

        cot.detail.contact.setcallsign("test-callsign")

        return cot

    def VideoStream(self):
        """
        this method generates a VideoStream CoT

        """

        cot = Event.VideoStream()

        cot.setuid(str(uuid4()))

        cot.detail._video.ConnectionEntry.setaddress("127.0.0.1")
        cot.detail._video.ConnectionEntry.setalias("test-cot")
        cot.detail.contact.setcallsign("test-cot")
        cot.detail._video.ConnectionEntry.setpath("/test-path")
        cot.detail._video.ConnectionEntry.setport("1111")
        cot.detail._video.ConnectionEntry.setprotocol("rtsp")
        cot.detail._video.seturl("127.0.0.1" + ":" + "1111" + "/test-path")
        del cot.detail.marti

        return cot