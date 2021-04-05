from FreeTAKServer.model.RestMessages.Route import Route, RestEnumerations

class RoutePost(Route):
    def __init__(self):
        pass

    def setlatitude(self, latitude):
        self.latitude = str(latitude)

    def getlatitude(self):
        return self.latitude

    def getlongitude(self):
        return self.longitude

    def setlongitude(self, longitude):
        self.longitude = str(longitude)

    def setlatitudeDest(self, latitudeDest: str):
        self.latitudeDest = str(latitudeDest)

    def getlatitudeDest(self):
        return self.latitudeDest

    def getlongitudeDest(self):
        return self.longitudeDest

    def setlongitudeDest(self, longitudeDest):
        self.longitudeDest = str(longitudeDest)

    def getrouteName(self):
        return self.routeName

    def setrouteName(self, name):
        self.routeName = name

    def setstartName(self, name):
        self.startName = name

    def getstartName(self):
        return self.startName

    def setendName(self, endName):
        self.endName = endName

    def getendName(self):
        return self.endName

    def gettimeout(self):
        return self.timeout

    def settimeout(self, timeout):
        self.timeout = timeout

    def getaddress(self):
        return self.address

    def setaddress(self, address):
        self.address = address

    def getmethod(self):
        return self.method

    def setmethod(self, method):
        self.method = method