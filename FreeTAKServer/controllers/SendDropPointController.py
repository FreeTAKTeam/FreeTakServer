from FreeTAKServer.controllers.model.SendDropPoint import SendDropPoint
from lxml import etree
from FreeTAKServer.controllers.model.Event import Event

class SendDropPointController:
    def __init__(self, RawCoT):
        self.Event = Event.dropPoint(etree.fromstring(RawCoT.xmlString))
        self.m_sendDropPoint = SendDropPoint()
        self.m_sendDropPoint.clientInformation = RawCoT.clientInformation
        self.m_sendDropPoint.xmlString = RawCoT.xmlString
        self.m_sendDropPoint.modelObject = self.Event
        print('drop point triggered')

    def getObject(self):
        return self.m_sendDropPoint