from FreeTAKServer.components.extended.excheck.persistence.templateInstanceContents import templateInstanceContents
import datetime as dt

class templateInstance:
    def __init__(self):
        self.name = "exchecktemplates"
        self.description = ""
        self.chatRoom = ""
        self.tool = "ExCheck"
        self.keywords = []
        self.creatorUid = "ExCheck"
        self.createTime = ""
        self.externalData = []
        self.uids = []
        self.contents = []
        self.setcreateTime()

    def setcontents(self, content):
        if isinstance(content, templateInstanceContents):
            self.contents.append(content)
        else:
            raise Exception("invalid type passed to setcontents this setter only accepts templateInstanceContentsJson instances")

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def setdescription(self, description):
        self.description = description

    def getdescription(self):
        return self.description

    def setcreateTime(self, createTime=None):
        DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if createTime == None:
            timer = dt.datetime
            now = timer.utcnow()
            zulu = now.strftime(DATETIME_FMT)
            self.createTime = zulu
        else:
            self.createTime = createTime