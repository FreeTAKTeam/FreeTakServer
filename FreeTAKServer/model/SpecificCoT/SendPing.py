from .SpecificCoTAbstract import SpecificCoTAbstract


class SendPing(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("ping")
