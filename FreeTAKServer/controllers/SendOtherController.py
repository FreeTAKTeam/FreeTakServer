from lxml import etree
from model.Event import Event
from model.SendOther import SendOther

class SendOtherController:
    #TODO: format needs to fixed as to make it consistent with the format of SendEmergency
    def __init__(self, RawCoT):
        
        self.m_SendOther = SendOther()
        self.m_SendOther.clientInformation = RawCoT.clientInformation
        self.m_SendOther.modelObject = Event('other')
        self.instantiateDomainModel(RawCoT)
        self.m_SendOther.xmlString = RawCoT.xmlString

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
            self.m_SendOther.modelObject.m_detail.Marti.m_Dest.callsign = dest.attrib['callsign']
            self.martiPresent = True
    
    def getObject(self):
        return self.m_SendOther