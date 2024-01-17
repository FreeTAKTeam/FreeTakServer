class EventVariables:

    @classmethod
    def drop_point(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = "h-g-i-g-o"
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def geochat(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = None
        cls.TYPE = "b-t-f"
        cls.HOW = 'h-g-i-g-o'
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def other(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = None
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def FederatedCoT(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = None
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def emergency_on(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = None
        cls.TYPE = "b-a-o-tbl"
        cls.HOW = 'm-g'
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def emergency_off(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = 'h-e'
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def connection(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = None
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def ping(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = None
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def disconnect(cls):
        cls.uid = None
        cls.version = '2.0'
        cls.type = 't-x-d-d'
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = 'h-g-i-g-o'
        return cls

    @classmethod
    def DeleteVideo(cls):
        cls.uid = None
        cls.version = '2.0'
        cls.type = 't-x-d-d'
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = 'h-g-i-g-o'
        return cls

    @classmethod
    def takPong(cls):
        cls.version = '2.0'
        cls.uid = 'takPong'
        cls.type = 't-x-c-t-r'
        cls.how = 'h-g-i-g-o'
        cls.time = None
        cls.start = None
        cls.stale = None
        return cls

    @classmethod
    def UserUpdate(cls):
        cls.version = None
        cls.uid = None
        cls.type = None
        cls.how = None
        cls.time = None
        cls.start = None
        cls.stale = None
        return cls

    @classmethod
    def SimpleCoT(cls):
        cls.version = "2.0"
        cls.uid = None
        cls.type = None
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = None
        return cls

    @classmethod
    def Presence(cls):
        cls.version = "2.0"
        cls.uid = None
        cls.type = None
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = None
        return cls

    @classmethod
    def ExcheckUpdate(cls):
        cls.version = None
        cls.uid = None
        cls.type = "t-x-m-c"
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = "h-g-i-g-o"
        return cls

    @classmethod
    def Route(cls):
        cls.version = None
        cls.uid = None
        cls.type = "b-m-r"
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = "h-e"
        return cls

    @classmethod
    def VideoStream(cls):
        cls.version = None
        cls.uid = None
        cls.type = "b-i-v"
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = "m-g"
        return cls

    @classmethod
    def DroneSensor(cls):
        cls.version = None
        cls.uid = None
        cls.type = "a-f-A-M-H-Q"
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = "m-g"
        return cls

    @classmethod
    def BitsImageryVideo(cls):
        cls.version = None
        cls.uid = None
        cls.type = "b-i-v"
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = "m-g"
        return cls

    @classmethod
    def SPISensor(cls):
        cls.version = None
        cls.uid = None
        cls.type = "b-m-p-s-p-i"
        cls.time = None
        cls.start = None
        cls.stale = None
        cls.how = "m-g"
        return cls