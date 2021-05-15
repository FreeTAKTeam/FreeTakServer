class statusVariables:
    def __init__(self):
        self.BATTERY = None
        self.READINESS = None

    @classmethod
    def drop_point(cls):
        cls.BATTERY = None
        cls.READINESS = "true"
        return cls

    @classmethod
    def connection(cls):
        cls.BATTERY = '100'
        cls.READINESS = "true"
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.battery = None
        return cls
