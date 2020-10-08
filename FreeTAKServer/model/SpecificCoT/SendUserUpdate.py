from .SpecificCoTAbstract import SpecificCoTAbstract

class SendUserUpdate(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("UserUpdate")
