from .SpecificCoTAbstract import SpecificCoTAbstract

class SendSPISensor(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("SPISensor")