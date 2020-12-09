from FreeTAKServer.controllers.BasicModelInstantiate import BasicModelInstantiate
from FreeTAKServer.controllers.model.Event import Event
from lxml import etree
from FreeTAKServer.controllers.model.SendEmergency import SendEmergency
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

class SendEmergencyController(BasicModelInstantiate):
    def __init__(self, RawCoT):
        self.SendEmergency = SendEmergency()
        self.SendEmergency.status = RawCoT.status
        self.SendEmergency.placeInInternalArray = True
        self.SendEmergency.clientInformation = RawCoT.clientInformation
        self.SendEmergency.modelObject = self.instantiateDomainModel(RawCoT)
        self.SendEmergency.xmlString = XMLCoTController().serialize_model_to_CoT(self.SendEmergency.modelObject,
                                                                                 'event')

    def instantiateDomainModel(self, RawCoT):
        if RawCoT.status == 'on':
            tempObject = Event.emergecyOn()
            modelObject = XMLCoTController().serialize_CoT_to_model(tempObject, RawCoT.xmlString)

        elif RawCoT.status == 'off':
            tempObject = Event.emergecyOff()
            modelObject = XMLCoTController().serialize_CoT_to_model(tempObject, RawCoT.xmlString)

        return modelObject
    
    def getObject(self):
        return self.SendEmergency