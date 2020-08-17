from .UidVariables import UidVariables as vars

class Uid:
    def __init__(self):
        self.Droid = None

    @staticmethod
    def connection(DROID = vars.connection().DROID):
        uid = Uid()
        uid.setDroid(DROID)
        return uid

    def getDroid(self):
        return self.Droid

    def setDroid(self, Droid = None):
        self.Droid = Droid
