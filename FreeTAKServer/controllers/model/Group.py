class Group:
    def __init__(self, xml):
        self.name = ''
        self.role = ''
        self.setname(xml.get('name'))
        self.setrole(xml.get('role'))

    def getrole(self):
        return self.role

    def setrole(self, role):
        self.role = role

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name
