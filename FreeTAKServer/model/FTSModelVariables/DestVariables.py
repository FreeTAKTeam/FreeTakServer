class DestVariables:
    def __init__(self):
        self.CALLSIGN = None

    @classmethod
    def geochat(cls):
        cls.CALLSIGN = None
        return cls

    @classmethod
    def other(cls):
        cls.CALLSIGN = None
        return cls