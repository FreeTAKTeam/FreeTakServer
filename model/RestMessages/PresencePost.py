from FreeTAKServer.model.RestMessages.Presence import Presence, RestEnumerations

class PresencePost(Presence):
    def __init__(self):
        pass

    def setuid(self, uid):
        self.uid = uid

    def getuid(self):
        try:
            return self.uid
        except:
            return None
    def sethow(self, how):
        self.how = RestEnumerations.how[how]
    
    def gethow(self):
        return self.how
    
    def setlatitude(self, latitude):
        self.latitude = str(latitude)

    def getlatitude(self):
        return self.latitude

    def setlongitude(self, longitude):
        self.longitude = str(longitude)

    def getlongitude(self):
        return self.longitude
    
    def setname(self, name):
        self.name = str(name)

    def getname(self):
        return self.name
    
    def setrole(self, role):
        self.role = RestEnumerations.roles[role]

    def getrole(self):
        return self.role
    
    def setteam(self, team):
        self.team = RestEnumerations.Teams[team]

    def getteam(self):
        return self.team

    def settimeout(self, timeout):
        self.timeout = timeout

    def gettimeout(self):
        return self.timeout