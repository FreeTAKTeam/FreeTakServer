class TrackVariables:
    def __init__(self):
        self.COURSE = None
        self.SPEED = None

    @classmethod
    def connection(cls):
        cls.SPEED = None
        cls.COURSE = None
        cls.SLOPE = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.speed = None
        cls.course = None
        cls.SLOPE = None
        return cls

    @classmethod
    def DroneSensor(cls):
        cls.SPEED = "-0.00"
        cls.COURSE = "46"
        cls.SLOPE = "0.00"
        return cls