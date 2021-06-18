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
        cls.north = None
        cls.roll = "0.0"
        cls.range = None
        cls.azimuth = "0.0"
        cls.model = "Drone Camera"
        cls.fov = None
        cls.type = "r-e"
        cls.version = "1.0"
        return cls