class TrackVariables:
    def __init__(self):
        self.COURSE = None
        self.SPEED = None

    @classmethod
    def connection(cls):
        cls.SPEED = None
        cls.COURSE = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.speed = None
        cls.course = None
        return cls