from lxml import etree
from FreeTAKServer.controllers.model.SendGeoChat import SendGeoChat
from FreeTAKServer.controllers.model.Event import Event

class SendGeoChatController:
    def __init__(self, RawCoT):
        self.m_SendGeoChat = SendGeoChat()
        self.m_SendGeoChat.clientInformation = RawCoT.clientInformation
        self.m_SendGeoChat.modelObject = Event.GeoChat(etree.fromstring(RawCoT.xmlString))
        self.m_SendGeoChat.xmlString = RawCoT.xmlString

    def getObject(self):
        return self.m_SendGeoChat