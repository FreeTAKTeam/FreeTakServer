from BasicModelInstantiate import BasicModelInstantiate
from model.Event import Event
from lxml import etree
from model.SendEmergency import SendEmergency
class SendEmergencyController(BasicModelInstantiate):
    def __init__(self, RawCoT):
        self.m_SendEmergency = SendEmergency()
        self.m_SendEmergency.status =  RawCoT.status
        self.m_SendEmergency.placeInInternalArray = True
        self.m_SendEmergency.clientInformation = RawCoT.clientInformation
        self.m_SendEmergency.modelObject = self.instantiateDomainModel(RawCoT)
        self.m_SendEmergency.xmlString = RawCoT.xmlString

            #instantiate model

    def instantiateDomainModel(self, RawCoT):
        if RawCoT.status == 'on':
            self.modelObject = Event("emergencyOn")
            root = RawCoT.xmlString
            #establish variables
            self.event = etree.XML(root)
            self.detail = self.event.find('detail')
            self.link = self.detail.find('link')
            self.contact = self.detail.find('contact')
            self.emergency = self.detail.find('emergency')
            
            #instantiate model
            self.eventAtrib()
            self.linkAtrib()
            self.contactAtrib()
            self.emergencyAtrib()

        elif RawCoT.status == 'off':
            self.modelObject = Event("emergencyOff")
            root = RawCoT.xmlString
            RawCoT.xmlString = root

            #establish variables
            self.event = etree.XML(root)
            self.detail = self.event.find('detail')
            self.emergency = self.detail.find('emergency')
            self.point = self.event.find('point')

            #instantiate model
            self.eventAtrib()
            self.pointAtrib()
            self.emergencyAtrib()
        return self.modelObject
    
    def getObject(self):
        return self.m_SendEmergency
        
if __name__ == "__main__":
    from model.RawCoT import RawCoT
    RawCoT = RawCoT()
    RawCoT.CoTType = 'emergency'
    RawCoT.clientInformation = "default"
    RawCoT.xmlString = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><event version="2.0" uid="19027743142-9-1-1" type="b-a-o-tbl" time="2020-06-06T13:32:44.026Z" start="2020-06-06T13:32:44.026Z" stale="2020-06-06T13:32:54.026Z" how="m-g"><point lat="43.855675" lon="-66.108009" hae="24.39561817703199" ce="11.7" le="9999999.0"/><detail><link uid="ANDROID-359975090666199" type="a-f-G-U-C" relation="p-p"/><contact callsign="SUMMER-Alert"/><emergency type="911 Alert">SUMMER</emergency></detail></event>'
    RawCoT.disconnect = 0
    RawCoT.status = 'on'
    x = SendEmergencyController(RawCoT).instantiateDomainModel(RawCoT)
    pass