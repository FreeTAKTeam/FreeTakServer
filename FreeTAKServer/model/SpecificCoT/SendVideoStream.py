from .SpecificCoTAbstract import SpecificCoTAbstract

class SendVideoStream(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("VideoStream")