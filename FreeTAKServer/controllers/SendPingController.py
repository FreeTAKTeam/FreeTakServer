from FreeTAKServer.controllers.BasicModelInstantiate import BasicModelInstantiate
from FreeTAKServer.controllers.model.SendPing import SendPing
from lxml import etree
from FreeTAKServer.controllers.model.Event import Event

class SendPingController():
    def __init__(self, RawCoT):
        self.Event = Event.Ping(etree.fromstring(RawCoT.xmlString))
        self.m_sendPing = SendPing()
        self.m_sendPing.clientInformation = RawCoT.clientInformation
        self.m_sendPing.xmlString = RawCoT.xmlString
        self.m_sendPing.modelObject = self.Event

    def getObject(self):
        return self.m_sendPing