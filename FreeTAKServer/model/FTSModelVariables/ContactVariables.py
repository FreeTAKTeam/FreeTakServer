class ContactVariables:
    def __init__(self):
        self.CALLSIGN = None
        self.ENDPOINT = None
        self.ICONSETPATH = None
        self.UID = None
        self.NAME = None

    @classmethod
    def connection(cls):
        cls.CALLSIGN = None
        cls.ENDPOINT = None
        cls.ICONSETPATH = None
        cls.UID = None
        cls.NAME = None
        return cls

    @classmethod
    def drop_point(cls):
        cls.CALLSIGN = "DEFAULT"
        cls.ENDPOINT = None
        cls.ICONSETPATH = None
        cls.UID = None
        cls.NAME = None
        return cls

    @classmethod
    def geochat(cls):
        cls.CALLSIGN = "DEFAULT"
        cls.ENDPOINT = None
        cls.ICONSETPATH = None
        cls.UID = None
        cls.NAME = None
        return cls

    @classmethod
    def emergency_on(cls):
        cls.CALLSIGN = None
        cls.ENDPOINT = None
        cls.ICONSETPATH = None
        cls.UID = None
        cls.NAME = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.endpoint = None
        cls.phone = None
        cls.callsign = None
        return cls

    @classmethod
    def SimpleCoT(cls):
        cls.callsign = None
        return cls

    @classmethod
    def Presence(cls):
        cls.callsign = None
        return cls
