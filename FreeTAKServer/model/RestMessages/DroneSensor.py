class DroneSensor:

    latitude = "0"

    longitude = "0"

    name = None

    Range = "300"

    Bearing = "0"

    FieldOfView = "80.0"

    VideoURLUID = None

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

    def getVideoURLUID(self):
        return self.VideoURLUID