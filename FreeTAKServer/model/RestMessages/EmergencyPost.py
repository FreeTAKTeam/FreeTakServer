from FreeTAKServer.model.RestMessages.Emergency import Emergency

class EmergencyPost(Emergency):
    def __init__(self):
        pass

    def setaddress(self, address):
        self.address = address

    def getaddress(self):
        try:
            return self.address
        except:
            return None

    def setemergencyType(self, emergencyType):
        self.emergencyType = emergencyType

    def getemergencyType(self):
        return self.emergencyType

    def setname(self, name):
        self.name = name

    def getname(self):
        return self.name

    def setlatitude(self, latitude):
        self.latitude = str(latitude)

    def getlatitude(self):
        if self.latitude == '':
            return '0'
        else:

            return self.latitude

    def setlongitude(self, longitude):
        self.longitude = str(longitude)

    def getlongitude(self):
        if self.longitude == '':
            return '0'
        else:
            return self.longitude
