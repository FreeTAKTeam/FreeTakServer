from lxml import etree
from model.Event import Event
from model.SendOther import SendOther

class SendOtherController:

    def __init__(self):
        self.type = "other"
        self.martiPresent = False
        self.m_Event = Event('other')
        self.m_SendOther = SendOther()

    def instantiateDomainModel(self, CoT):
        self.m_SendOther.xmlString = CoT.xmlString
        self.m_SendOther.clientInformation = CoT.clientInformation

        xml = etree.fromstring(CoT.xmlString)

        detail = xml.find('detail')
        marti = detail.find('marti')
        #check for marti and dest
        if marti == None:
            pass
        else:
            dest = marti.find('dest')
            self.m_Event.m_detail.m_marti.m_dest.callsign = dest.attrib['callsign']
            self.martiPresent = True
        self.m_SendOther.modelObject = self.m_Event
        return self.m_SendOther