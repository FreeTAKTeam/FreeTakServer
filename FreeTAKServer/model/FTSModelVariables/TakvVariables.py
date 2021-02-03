class TakvVariables:
    def __init__(self):
        self.VERSION = None
        self.PLATFORM = None
        self.DEVICE = None
        self.OS = None

    @classmethod
    def connection(cls):
        cls.VERSION = None
        cls.PLATFORM = None
        cls.DEVICE = None
        cls.OS = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.device = None
        cls.platform = None
        cls.os = None
        cls.version = None
        return cls
