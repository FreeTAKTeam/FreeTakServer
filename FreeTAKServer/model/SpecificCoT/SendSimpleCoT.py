from .SpecificCoTAbstract import SpecificCoTAbstract

class SendSimpleCoT(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("SimpleCoT")