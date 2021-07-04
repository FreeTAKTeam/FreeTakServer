class DroneSensor:

    timeout = None

    uid = None

    latitude = "0"

    longitude = "0"

    name = None

    Range = "300"

    Bearing = "0"

    FieldOfView = "80.0"

    VideoURLUID = None

    SPILongitude = None

    SPILatitude = None

    SPIName = None

    def settimeout(self, timeout):
        self.timeout = timeout

    def gettimeout(self):
        return self.timeout

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

    def getRange(self):
        return self.Range

    def setRange(self, Range):
        self.Range = Range

    def getBearing(self):
        return self.Bearing

    def setBearing(self, Bearing):
        self.Bearing = Bearing

    def getFieldOfView(self):
        return self.FieldOfView

    def setFieldOfView(self, FieldOfView):
        self.FieldOfView = FieldOfView

    def setVideoURLUID(self, VideoURLUID):
        self.VideoURLUID = VideoURLUID

    def getVideoURLUID(self):
        return self.VideoURLUID

    def getSPILatitude(self):
        return self.SPILatitude

    def setSPILatitude(self, SPILatitude):
        self.SPILatitude = SPILatitude

    def getSPILongitude(self):
        return self.SPILongitude

    def setSPILongitude(self, SPILongitude):
        self.SPILongitude = SPILongitude

    def getSPIName(self):
        return self.SPIName

    def setSPIName(self, Name):
        self.SPIName = Name

    def getuid(self):
        return self.uid

    def setuid(self, uid):
        self.uid = uid