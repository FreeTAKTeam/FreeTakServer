from FreeTAKServer.model.RestMessages.Chat import Chat

class ChatPost(Chat):
    def __init__(self):
        pass

    def messagesetter(self, message):
        self.message = message

    def messagegetter(self):
        return self.message

    def sendersetter(self, sender):
        self.sender = sender

    def sendergetter(self):
        return self.sender