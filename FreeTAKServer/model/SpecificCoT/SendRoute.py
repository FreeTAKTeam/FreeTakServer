from .SpecificCoTAbstract import SpecificCoTAbstract

class SendRoute(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("Route")