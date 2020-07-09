from .Group import Group

class Hierarchy:
    def __init__(self, xml):
        try:
            self.m_Group = Group(xml.find('group'))
        except:
            pass