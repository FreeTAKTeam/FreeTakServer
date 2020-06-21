from BasicModelInstantiate import BasicModelInstantiate
from FreeTAKServer.controllers.model.Event import Event
from lxml import etree
from FreeTAKServer.controllers.model.SendEmergency import SendEmergency
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