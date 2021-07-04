class SPISensor:
    uid = None

    latitude = "0"

    longitude = "0"

    name = None

    droneUid = None

    timeout = None

    def gettimeout(self):
        return self.timeout

    def settimeout(self, timeout):
        self.timeout = timeout

    def getuid(self):
        return self.uid

    def setuid(self, uid):
        self.uid = uid

    def getlatitude(self):
        return self.latitude

    def setlatitude(self, latitude):
        self.latitude = latitude

    def getlongitude(self):
        return self.longitude

    def setlongitude(self, longitude):
        self.longitude = longitude

    def getname(self):
        return self.name

    def setname(self, name):
        self.name = name

    def setdroneUid(self, uid):
        self.droneUid = uid

    def getdroneUid(self):
        return self.droneUid