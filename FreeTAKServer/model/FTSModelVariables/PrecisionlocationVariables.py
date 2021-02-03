class PrecisionlocationVariables:
    def __init__(self):
        self.ALTSRC = None
        self.GEOPOINTSRC = None

    @classmethod
    def drop_point(cls):
        cls.ALTSRC = '???'
        cls.GEOPOINTSRC = None
        return cls

    @classmethod
    def connection(cls):
        cls.ALTSRC = None
        cls.GEOPOINTSRC = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.altsrc = None
        cls.geopointsrc = None
        return cls
