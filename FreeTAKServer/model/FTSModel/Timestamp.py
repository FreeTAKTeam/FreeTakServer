from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.TimestampVariables import TimestampVariables as vars
import datetime as dt


class Timestamp(FTSProtocolObject):
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG, ):
        timestamp = Timestamp()

        timestamp.setINTAG(INTAG)

        return timestamp

    def setINTAG(self, INTAG=None):
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if INTAG is None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            self.INTAG = zulu
        else:
            self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG
