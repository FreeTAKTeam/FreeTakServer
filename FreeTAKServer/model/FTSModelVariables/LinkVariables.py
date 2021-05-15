class LinkVariables:
    def __init__(self):
        self.UID = None
        self.RELATION = None
        self.PRODUCTIONTIME = None
        self.TYPE = None
        self.PARENTCALLSIGN = None
        self.POINT = None

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
        cls.uid = None
        cls.type = "a-f-G-U-C"
        cls.relation = "p-p"
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