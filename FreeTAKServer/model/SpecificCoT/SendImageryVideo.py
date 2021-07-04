from .SpecificCoTAbstract import SpecificCoTAbstract

class SendImageryVideo(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("ImageryVideo")