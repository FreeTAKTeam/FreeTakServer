from FreeTAKServer.model.RestMessages.Chat import Chat


class ChatPost(Chat):

    def setmessage(self, message):
        self.message = message

    def getmessage(self):
        return self.message

    def setsender(self, sender):
        self.sender = sender

    def getsender(self):
        return self.sender
