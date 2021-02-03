from .SpecificCoTAbstract import SpecificCoTAbstract


class SendPresence(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("Presence")
