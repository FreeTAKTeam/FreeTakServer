from FreeTAKServer.model.SpecificCoT.SendSPISensor import SendSPISensor
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

class SendSPISensorController:

        def __init__(self, json):
            tempObject = event.SPISensor()
            object = SendSPISensor()
            object.setModelObject(tempObject)
            object.modelObject = self._serializeJsonToModel(object.modelObject, json)
            object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
            self.setCoTObject(object)

        def _serializeJsonToModel(self, object, json):
            if json.gettimeout():
                object.setstale(staletime=json.gettimeout())
            if json.getuid():
                object.setuid(json.getuid())
            if json.getlatitude():
                object.point.setlon(json.getlongitude())
            if json.getlatitude():
                object.point.setlat(json.getlatitude())
            if json.getname():
                object.detail.contact.setcallsign(json.getname())
            if json.getdroneUid():
                object.detail.link.setuid(json.getdroneUid())
            return object

        def setCoTObject(self, CoTObject):
            self.CoTObject = CoTObject

        def getCoTObject(self):
            return self.CoTObject