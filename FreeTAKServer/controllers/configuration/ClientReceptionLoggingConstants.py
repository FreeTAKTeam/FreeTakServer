from .LoggingConstants import LoggingConstants


class ClientReceptionLoggingConstants(LoggingConstants):
    def __init__(self):
        super().__init__()
        self.LOGNAME = "ClientHandler"
