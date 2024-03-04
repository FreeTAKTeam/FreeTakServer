class LinkVariables:
    def __init__(self):
        self.UID = None
        self.RELATION = None
        self.PRODUCTIONTIME = None
        self.TYPE = None
        self.PARENTCALLSIGN = None
        self.POINT = None

    @classmethod
    def VideoStream(cls):
        cls.UID = None
        cls.PRODUCTIONTIME = None
        cls.RELATIONSHIP = None
        cls.PARENTCALLSIGN = None
        return cls

    @classmethod
    def drop_point(cls):
        cls.UID = "DEFAULT"
        cls.TYPE = "a-f-G-U-C"
        cls.PARENTCALLSIGN = "DEFAULT"
        cls.RELATION = "p-p"
        cls.PRODUCTIONTIME = None
        return cls

    @classmethod
    def geochat(cls):
        cls.UID = "SERVER-UID"
        cls.TYPE = "a-f-G-U-C-I"
        cls.PARENTCALLSIGN = None
        cls.RELATION = "p-p"
        return cls

    @classmethod
    def emergency_on(cls):
        cls.UID = "SERVER"
        cls.TYPE = "a-f-G-U-C"
        cls.PARENTCALLSIGN = None
        cls.RELATION = "p-p"
        cls.PRODUCTIONTIME = None
        return cls

    @classmethod
    def disconnect(cls):
        cls.UID = None
        cls.TYPE = "a-f-G-U-C"
        cls.RELATION = "p-p"
        return cls

    @classmethod
    def DeleteVideo(cls):
        cls.UID = None
        cls.TYPE = "b-i-v"
        cls.RELATION = "p-p"
        return cls

    @classmethod
    def Route(cls):
        cls.UID = None
        cls.TYPE = "b-m-p-w"
        cls.REMARKS = ""
        cls.POINT = "0, 0"
        cls.CALLSIGN = ""
        cls.RELATION = "c"
        return cls

    @classmethod
    def SPISensor(cls):
        cls.UID = None
        cls.TYPE = "a-f-A-M-H-Q"
        cls.RELATION = "p-p"
        return cls

    @classmethod
    def BitsImageryVideo(cls):
        cls.UID = None
        cls.PRODUCTIONTIME = None
        return cls