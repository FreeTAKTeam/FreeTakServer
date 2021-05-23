class ConnectionEntryVariables:

    def __init__(self):
        self.networkTimeout = None
        self.uid = None
        self.path = None
        self.protocol = None
        self.bufferTime = None
        self.address = None
        self.port = None
        self.roverPort = None
        self.rtspReliable = None
        self.ignoreEmbeddedKLV = None
        self.alias = None

    @classmethod
    def VideoStream(cls):
        cls.networkTimeout = None
        cls.uid = None
        cls.path = None
        cls.protocol = None
        cls.bufferTime = None
        cls.address = None
        cls.port = None
        cls.roverPort = None
        cls.rtspReliable = None
        cls.ignoreEmbeddedKLV = None
        cls.alias = None
        return cls
