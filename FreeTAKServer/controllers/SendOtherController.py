from lxml import etree
from FreeTAKServer.controllers.model.SendOther import SendOther
from FreeTAKServer.controllers.model.Event import Event
class SendOtherController:
    #TODO: format needs to fixed as to make it consistent with the format of SendEmergency
    def __init__(self, RawCoT):
        self.m_SendOther = SendOther()
        self.m_SendOther.clientInformation = RawCoT.clientInformation
        self.m_SendOther.modelObject = Event.Other(etree.fromstring(RawCoT.xmlString), RawCoT.clientInformation)
        self.m_SendOther.xmlString = RawCoT.xmlString
    
    def getObject(self):
        return self.m_SendOther