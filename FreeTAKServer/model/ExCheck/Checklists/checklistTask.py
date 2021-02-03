class checklistTask:
    def __init__(self):
        self.lineBreak = "false"
        self.number = 0
        self.uid = ''
        self.status = 'Pending'

    def setuid(self, uid):
        self.uid = uid

    def getuid(self):
        return self.uid

    def getlineBreak(self):
        return self.lineBreak

    def setlineBreak(self, lineBreak):
        self.lineBreak = lineBreak

    def setnumber(self, number):
        self.number = number

    def getnumber(self):
        return self.number

    def setstatus(self, status):
        self.status = status

    def getstatus(self):
        return self.status
