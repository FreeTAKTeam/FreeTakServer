class _GroupVariables:
    def __init__(self):
        self.NAME = None
        self.ROLE = None

    @classmethod
    def connection(cls):
        cls.NAME = None
        cls.ROLE = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.name = None
        cls.role = None
        return cls

    @classmethod
    def Presence(cls):
        cls.name = None
        cls.role = None
        return cls