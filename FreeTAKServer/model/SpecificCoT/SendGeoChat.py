from .SpecificCoTAbstract import SpecificCoTAbstract

class SendGeoChat(SpecificCoTAbstract):
    def __init__(self):
        self.define_variables()
        self.setType("GeoChat")