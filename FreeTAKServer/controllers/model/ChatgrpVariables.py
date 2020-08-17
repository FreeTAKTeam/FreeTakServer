class ChatgrpVariables:

    def __init__(self):
        self.ID = None
        self.UID0 = None
        self.UID1 = None

    @classmethod
    def geochat(cls):
        cls.ID = "SERVER-UID"
        cls.UID1 = "All Chat Rooms"
        cls.UID0 = "SERVER-UID"
        return cls