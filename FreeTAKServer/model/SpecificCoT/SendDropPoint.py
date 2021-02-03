from .SpecificCoTAbstract import SpecificCoTAbstract


class SendDropPoint(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("DropPoint")
