from FreeTAKServer.model.RestMessages.GeoObject import GeoObject, RestEnumerations

class GeoObjectPost(GeoObject):
    def __init__(self):
        pass

    def setaddress(self, address):
        self.address = address

    def getaddress(self):
        try:
            return self.address
        except:
            return None

    def setuid(self, uid):
        self.uid = uid

    def getuid(self):
        try:
            return self.uid
        except:
            return None

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

    def setremarks(self, remarks):
        self.remarks = remarks

    def getremarks(self):
        return self.remarks

    def setrepeat(self, repeat: bool):
        """the new repeat value for this instance

        Args:
            repeat (bool): whether or not the message should be repeated
        """
        self.repeat = repeat
        
    def getrepeat(self) -> bool:
        """get the repeat value for this instance

        Returns:
            bool: whether or not the geo object should be repeated 
        """
        return self.repeat