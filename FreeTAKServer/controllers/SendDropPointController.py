from FreeTAKServer.controllers.model.SendDropPoint import SendDropPoint
from lxml import etree
from FreeTAKServer.controllers.model.Event import Event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

class SendDropPointController:
    def __init__(self, RawCoT):
        tempObject = Event.dropPoint()
        self.sendDropPoint = SendDropPoint()
        self.sendDropPoint.clientInformation = RawCoT.clientInformation
        self.sendDropPoint.modelObject = XMLCoTController().serialize_CoT_to_model(tempObject, etree.fromstring(RawCoT.xmlString))
        self.sendDropPoint.xmlString = XMLCoTController().serialize_model_to_CoT(self.sendDropPoint.modelObject, 'event')

    def getObject(self):
        return self.sendDropPoint