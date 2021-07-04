from .SpecificCoTAbstract import SpecificCoTAbstract

class SendDeleteVideoStream(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("DeleteVideoStream")