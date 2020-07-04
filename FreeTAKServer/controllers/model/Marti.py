from .Dest import Dest

class Marti:
    def __init__(self, xml):
        self.m_Dest = Dest(xml.find('dest'))