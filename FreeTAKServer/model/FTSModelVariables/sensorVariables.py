class sensorVariables:

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

    @classmethod
    def DroneSensor(cls):
        cls.elevation = "0.0"
        cls.vfov = "60"
        cls.north = "227"
        cls.roll = "0.0"
        cls.range = None
        cls.azimuth = "46"
        cls.model = "Drone Camera"
        cls.fov = None
        cls.type = "r-e"
        cls.version = "0.6"
        return cls