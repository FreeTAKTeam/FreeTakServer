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
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = None
        cls.TIME = None
        cls.START = None
        cls.STALE = None
        return cls

    @classmethod
    def emergency_off(cls):
        cls.VERSIONNUM = '2.0'
        cls.UID = 'RANDOM'
        cls.TYPE = "DEFAULT"
        cls.HOW = None
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