class Uid:
    def __init__(self, xml):
        self.Droid = None
        self.setDroid(xml.get('Droid'))
    def getDroid(self):
        return self.Droid
    def setDroid(self, Droid):
        self.Droid = Droid
