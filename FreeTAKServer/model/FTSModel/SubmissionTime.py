from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.SubmissionTimeVariables import SubmissionTimeVariables as vars
import datetime as dt

class SubmissionTime(FTSProtocolObject):
    def __init__(self):
        self.INTAG = None

    @staticmethod
    def ExcheckUpdate(INTAG=vars.ExcheckUpdate().INTAG, ):
        submissiontime = SubmissionTime()

        submissiontime.setINTAG(INTAG)

        return submissiontime

    def setINTAG(self, INTAG=None):
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if INTAG == None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            self.INTAG = zulu
        else:
            self.INTAG = INTAG

    def getINTAG(self):
        return self.INTAG