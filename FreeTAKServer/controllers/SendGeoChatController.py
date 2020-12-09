from lxml import etree
from FreeTAKServer.controllers.model.SendGeoChat import SendGeoChat
from FreeTAKServer.controllers.model.Event import Event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

class SendGeoChatController:
    def __init__(self, RawCoT):
        self.SendGeoChat = SendGeoChat()
        tempobject = Event.GeoChat()
        self.SendGeoChat.clientInformation = RawCoT.clientInformation
        self.SendGeoChat.modelObject = XMLCoTController().serialize_CoT_to_model(tempobject, etree.fromstring(RawCoT.xmlString))
        self.SendGeoChat.xmlString = XMLCoTController().serialize_model_to_CoT(self.SendGeoChat.modelObject, 'event')

    def getObject(self):
        return self.SendGeoChat