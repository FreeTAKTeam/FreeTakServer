from .SpecificCoTAbstract import SpecificCoTAbstract
class SendChecklist(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("Checklist")