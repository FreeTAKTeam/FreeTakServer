class EmergencyVariables:
    def __init__(self):
        self.TYPE = None
        self.ALERT = None
        # if true the Emergency beacon is canceled
        self.CANCEL = None

    @classmethod
    def emergency_on(cls):
        cls.CANCEL = None
        cls.ALERT = None
        cls.TYPE = None
        cls.INTAG = None
        return cls

    @classmethod
    def emergency_off(cls):
        cls.CANCEL = None
        cls.INTAG = None
        return cls