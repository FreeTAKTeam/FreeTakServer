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
        return cls