class checklistDetails:
    def __init__(self):
        self.name = ''
        self.uid = ''
        self.description = ''
        self.startTime = ''
        self.creatorUid = ''
        self.creatorCallsign = ''

    def setname(self, name = None):
        self.name = name

    def getname(self):
        return self.name

    def setcreatorUid(self, creatoruid):
        self.creatorUid = creatoruid

    def getcreatorUid(self):
        return self.creatorUid

    def setcreatorCallsign(self, creatorCallsign):
        self.creatorCallsign = creatorCallsign

    def getcreatorCallsign(self):
        return self.creatorCallsign

    def setuid(self, uid):
        self.uid = uid

    def getuid(self):
        return self.uid

    def setstartTime(self, startTime):
        self.startTime = startTime

    def getstartTime(self):
        return self.startTime