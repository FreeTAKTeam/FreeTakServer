from FreeTAKServer.model.RestMessages.GeoObject import GeoObject, RestEnumerations


class GeoObjectPost(GeoObject):
    def __init__(self):
        pass

    def setattitude(self, attitude):
        self.attitude = RestEnumerations.attitude[attitude]

    def getattitude(self):
        return self.attitude

    def setgeoObject(self, geoObject):
        self.geoObject = RestEnumerations.supportedTypeEnumerations[geoObject]

    def getgeoObject(self):
        return self.geoObject

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

    def settimeout(self, timeout):
        self.timeout = int(timeout)

    def gettimeout(self):
        return self.timeout
