from lxml import etree
from FreeTAKServer.controllers.model.SendOther import SendOther
from FreeTAKServer.controllers.model.Event import Event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

class SendOtherController:
    #TODO: format needs to fixed as to make it consistent with the format of SendEmergency
    def __init__(self, RawCoT):
        self.SendOther = SendOther()
        tempObject = Event.Other()
        self.SendOther.clientInformation = RawCoT.clientInformation
        filtered_CoT = self.filter_CoT(etree.fromstring(RawCoT.xmlString))
        self.SendOther.modelObject = XMLCoTController().serialize_CoT_to_model(tempObject, filtered_CoT)
        self.SendOther.xmlString = RawCoT.xmlString
    
    def getObject(self):
        return self.SendOther

    #this function modifies the CoT so only the marti and point tags are present
    def filter_CoT(self, event):
        outputEvent = etree.Element('event')

        point = event.find('point')
        outputEvent.append(point)

        detail = event.find('detail')

        try:
            marti = detail.find('marti')
            outputDetail = etree.SubElement(outputEvent, 'detail')
            outputDetail.append(marti)
        except:
            etree.SubElement(outputEvent, 'detail')

        return outputEvent
