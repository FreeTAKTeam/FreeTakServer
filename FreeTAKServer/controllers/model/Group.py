from .Contact import Contact

class Group:
    def __init__(self, xml):
        self.uid = None
        self.name = None
        self.setuid(xml.get('uid'))
        self.setname(xml.get('name'))
        try:
            self.m_Contact = Contact(xml.find('contact'))
        except:
            pass
        try:
            self.m_Group = Group(xml.find('group'))
        except:
            pass

    def setuid(self, uid=None):
        self.uid = uid
        
    def getuid(self):
        return self.uid

    def setname(self, name=None):
        self.name = name

    def getname(self):
        return self.name