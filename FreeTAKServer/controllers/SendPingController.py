from FreeTAKServer.controllers.BasicModelInstantiate import BasicModelInstantiate
from FreeTAKServer.controllers.model.SendPing import SendPing
from lxml import etree
from FreeTAKServer.controllers.model.Event import Event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

class SendPingController():
    def __init__(self, RawCoT):
        tempObject = Event.Ping()
        self.sendPing = SendPing()
        self.sendPing.clientInformation = RawCoT.clientInformation
        self.sendPing.modelObject = XMLCoTController().serialize_CoT_to_model(tempObject, etree.fromstring(RawCoT.xmlString))
        self.sendPing.xmlString = XMLCoTController().serialize_model_to_CoT(self.sendPing.modelObject, 'event')

    def getObject(self):
        return self.sendPing