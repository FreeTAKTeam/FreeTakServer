from .SpecificCoTAbstract import SpecificCoTAbstract

class Presence(SpecificCoTAbstract):

    def __init__(self):
        self.define_variables()
        self.setType("Presence")