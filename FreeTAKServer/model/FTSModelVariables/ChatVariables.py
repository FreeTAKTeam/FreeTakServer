class ChatVariables:
    def __init__(self):
        self.SENDERCALLSIGN = None
        self.ID = None
        self.PARENT = None
        self.CHATROOM = None
        self.GROUPOWNER = None

    @classmethod
    def geochat(cls):
        cls.MESSAGEID = None
        cls.SENDERCALLSIGN = 'SERVER-UID'
        cls.ID = "All Chat Rooms"
        cls.PARENT = None
        cls.CHATROOM = "All Chat Rooms"
        cls.GROUPOWNER = "false"
        return cls