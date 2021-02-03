from .SpecificCoTAbstract import SpecificCoTAbstract


class SendDisconnect(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("Disconnect")
