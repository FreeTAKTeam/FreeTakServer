from .SpecificCoTAbstract import SpecificCoTAbstract


class SendOther(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("other")
        self.martiPresent = False

    def setMartiPresent(self, martiPresent):
        self.martiPresent = martiPresent

    def getMartiPresent(self):
        return self.martiPresent
