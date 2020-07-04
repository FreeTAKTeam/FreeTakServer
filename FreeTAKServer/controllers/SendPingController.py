from FreeTAKServer.controllers.BasicModelInstantiate import BasicModelInstantiate
from FreeTAKServer.controllers.model.SendPing import SendPing
from lxml import etree
from FreeTAKServer.controllers.model.Event import Event

class SendPingController(BasicModelInstantiate):
    def __init__(self, RawCoT):
        self.m_sendPing = SendPing()
        self.m_sendPing.clientInformation = RawCoT.clientInformation
        self.m_sendPing.xmlString = RawCoT.xmlString
        self.m_sendPing.Event = self.instantiateDomainModel(RawCoT)

    def instantiateDomainModel(self, RawCoT):
        xml = etree.fromstring(RawCoT.xmlString)
        return Event.Ping(xml)


    def getObject(self):
        return self.m_sendPing