from .SpecificCoTAbstract import SpecificCoTAbstract

class SendExcheckUpdate(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("ExcheckUpdate")