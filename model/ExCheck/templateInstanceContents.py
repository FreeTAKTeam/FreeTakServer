from FreeTAKServer.model.ExCheck.templateInstanceContentsData import templateInstanceContentsData
import datetime as dt

class templateInstanceContents:
    def __init__(self):
        self.data = templateInstanceContentsData()
        self.timestamp = ""
        self.creatorUid = ""
        self.settimestamp()
    def settimestamp(self, timestamp = None):
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if timestamp == None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            self.timestamp = zulu
        else:
            self.timestamp = timestamp

    def gettimestamp(self):
        return self.timestamp

    def setcreatoruid(self, creatoruid):
        self.creatorUid = creatoruid

    def getcreatoruid(self):
        return self.creatorUid