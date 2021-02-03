from .SpecificCoTAbstract import SpecificCoTAbstract


class SendTakPong(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("TakPong")
