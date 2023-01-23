class RemarksVariables:
    def __init__(self):
        self.TIME = None
        self.SOURCE = None
        self.SOURCEID = None
        self.INTAG = None

    @classmethod
    def drop_point(cls):
        cls.TIME = None
        cls.SOURCE = None
        cls.SOURCEID = None
        cls.INTAG = None
        return cls

    @classmethod
    def geochat(cls):
        cls.TIME = None
        cls.SOURCE = 'SERVER'
        cls.SOURCEID = None
        cls.INTAG = 'DEFAULT'
        cls.TO = 'All Chat Rooms'
        return cls

    @classmethod
    def emerygency_on(cls):
        cls.TIME = None
        cls.SOURCE = None
        cls.SOURCEID = None
        cls.INTAG = None
        return cls
