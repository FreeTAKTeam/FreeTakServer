class LinkVariables:
    def __init__(self):
        self.UID = None
        self.RELATION = None
        self.PRODUCTIONTIME = None
        self.TYPE = None
        self.PARENTCALLSIGN = None

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
        cls.UID = "DEFAULT"
        cls.TYPE = "a-f-G-U-C"
        cls.PARENTCALLSIGN = "DEFAULT"
        cls.RELATION = "p-p"
        cls.PRODUCTIONTIME = None
        return cls