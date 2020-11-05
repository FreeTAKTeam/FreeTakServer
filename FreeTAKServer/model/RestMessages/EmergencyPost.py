from FreeTAKServer.model.RestMessages.Emergency import Emergency, RestEnumerations

class EmergencyPost(Emergency):
    def __init__(self):
        pass

    def setemergencyType(self, emergencyType):
        self.emergencyType = RestEnumerations.emergencyTypes[emergencyType]

    def getemergencyType(self):
        return self.emergencyType

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def setlatitude(self, latitude):
        self.latitude = str(latitude)

    def getlatitude(self):
        return self.latitude

    def setlongitude(self, longitude):
        self.longitude = str(longitude)

    def getlongitude(self):
        return self.longitude

if __name__ == "__main__":
    x = EmergencyPost()
    1 == 1