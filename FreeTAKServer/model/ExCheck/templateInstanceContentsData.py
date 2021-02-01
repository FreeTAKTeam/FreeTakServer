import datetime as dt

class templateInstanceContentsData:
    def __init__(self):
        self.uid = ""
        self.filename = ""
        self.keywords = ["name", "description", "Callsign"]
        self.mimeType = "application/xml"
        self.name = ""
        self.submissionTime = ""
        self.submitter = ""
        self.hash = ""
        self.size = 0
        self.tool = ""
        self.creatorCallsign = ""

    def setfilename(self, filename = None):
        if filename is None:
            self.filename = self.uid+'.xml'
        else:
            self.filename = filename

    def getfilename(self):
        return self.filename

    def setname(self, name = None):
        if name is None:
            self.name = self.uid
        else:
            self.name = name

    def getname(self):
        return self.name

    def setsize(self, size):
        self.size = size

    def getsize(self):
        return self.size

    def setsubmitter(self, submitter):
        self.submitter = submitter

    def getsubmitter(self):
        return self.submitter

    def sethash(self, hash):
        self.hash = hash

    def gethash(self):
        return self.hash

    def setmimeType(self, mimeType):
        self.mimeType = mimeType

    def getmimeType(self):
        return self.mimeType

    def setkeywords(self, name = None, description = None, callsign = None):
        self.keywords[0] = name
        self.keywords[1] = description
        self.keywords[2] = callsign

    def settool(self,tool):
        self.tool = tool

    def setuid(self, uid):
        self.uid = uid

    def setsubmissionTime(self, timestamp = None):
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if timestamp == None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            self.submissionTime = zulu
        else:
            self.submissionTime = timestamp