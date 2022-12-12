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
        cls.PHONE = None
        cls.EMAILADDRESS = None
        cls.XMPPUSERNAME = None
        cls.SIPADDRESS = None
        return cls

    @classmethod
    def drop_point(cls):
        cls.CALLSIGN = "DEFAULT"
        cls.ENDPOINT = None
        cls.ICONSETPATH = None
        cls.UID = None
        cls.NAME = None
        cls.EMAILADDRESS = None
        cls.XMPPUSERNAME = None
        cls.SIPADDRESS = None
        return cls

    @classmethod
    def geochat(cls):
        cls.CALLSIGN = "DEFAULT"
        cls.ENDPOINT = None
        cls.ICONSETPATH = None
        cls.UID = None
        cls.NAME = None
        cls.EMAILADDRESS = None
        cls.XMPPUSERNAME = None
        cls.SIPADDRESS = None
        return cls

    @classmethod
    def emergency_on(cls):
        cls.CALLSIGN = None
        cls.ENDPOINT = None
        cls.ICONSETPATH = None
        cls.UID = None
        cls.NAME = None
        cls.EMAILADDRESS = None
        cls.XMPPUSERNAME = None
        cls.SIPADDRESS = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.ENDPOINT = None
        cls.PHONE = None
        cls.CALLSIGN = None
        cls.EMAILADDRESS = None
        cls.XMPPUSERNAME = None
        cls.SIPADDRESS = None
        return cls

    @classmethod
    def SimpleCoT(cls):
        cls.callsign = None
        return cls

    @classmethod
    def Presence(cls):
        cls.callsign = None
        return cls

    @classmethod
    def Route(cls):
        cls.callsign = None
        return cls

    @classmethod
    def VideoStream(cls):
        cls.callsign = None
        return cls

    @classmethod
    def DroneSensor(cls):
        cls.callsign = None
        return cls

    @classmethod
    def SPISensor(cls):
        cls.callsign = None
        return cls

    @classmethod
    def BitsImageryVideo(cls):
        cls.callsign = None
        return cls