from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from FreeTAKServer.model.FTSModelVariables.sensorVariables import sensorVariables as vars

class Sensor(FTSProtocolObject):
    def __init__(self):
        self.elevation = None
        self.vfov = None
        self.north = None
        self.roll = None
        self.range = None
        self.azimuth = None
        self.model = None
        self.fov = None
        self.type = None
        self.version = None

    @staticmethod
    def DroneSensor(ELEVATION=vars.DroneSensor().elevation, VFOV=vars.DroneSensor().vfov,
                    NORTH=vars.DroneSensor().north, ROLL=vars.DroneSensor().roll, RANGE=vars.DroneSensor().range,
                    AZIMUTH=vars.DroneSensor().azimuth, MODEL=vars.DroneSensor().model, FOV=vars.DroneSensor().fov,
                    TYPE=vars.DroneSensor().type, VERSION=vars.DroneSensor().version, ):
        sensor = Sensor()
        sensor.setelevation(ELEVATION)
        sensor.setvfov(VFOV)
        sensor.setnorth(NORTH)
        sensor.setroll(ROLL)
        sensor.setrange(RANGE)
        sensor.setazimuth(AZIMUTH)
        sensor.setmodel(MODEL)
        sensor.setfov(FOV)
        sensor.settype(TYPE)
        sensor.setversion(VERSION)

        return sensor

    def getelevation(self):
            return self.elevation

    def setelevation(self, elevation):
        self.elevation = elevation

    def getvfov(self):
            return self.vfov

    def setvfov(self, vfov):
        self.vfov = vfov

    def getnorth(self):
            return self.north

    def setnorth(self, north):
        self.north = north

    def getroll(self):
            return self.roll

    def setroll(self, roll):
        self.roll = roll

    def getrange(self):
            return self.range

    def setrange(self, range):
        self.range = range

    def getazimuth(self):
            return self.azimuth

    def setazimuth(self, azimuth):
        self.azimuth = azimuth

    def getmodel(self):
            return self.model

    def setmodel(self, model):
        self.model = model

    def getfov(self):
            return self.fov

    def setfov(self, fov):
        self.fov = fov

    def gettype(self):
            return self.type

    def settype(self, type):
        self.type = type

    def getversion(self):
            return self.version

    def setversion(self, version):
        self.version = version