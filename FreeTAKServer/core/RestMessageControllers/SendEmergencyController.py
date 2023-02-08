import uuid

from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
from FreeTAKServer.core.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.model.RestMessages.EmergencyDelete import EmergencyDelete
from FreeTAKServer.model.RestMessages.EmergencyPost import EmergencyPost
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.SpecificCoT.SendEmergency import SendEmergency

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendGeoChatController").getLogger()

from geopy import Nominatim


class SendEmergencyController:
    def __init__(self, json):
        if isinstance(json, EmergencyPost):
            tempObject = event.emergecyOn()
        elif isinstance(json, EmergencyDelete):
            tempObject = event.emergecyOff()
        else:
            raise Exception('unsupported object type passed under json argument')
        object = SendEmergency()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        # runs if emergency is on
        if isinstance(json, EmergencyPost):
            object.settype(RestEnumerations.emergencyTypes[json.getemergencyType()])
            object.detail.contact.setcallsign(json.getname())
            object.detail.emergency.settype(json.getemergencyType())
            object.detail.remarks.setINTAG(json.getremarks())
            if json.getaddress():
                locator = Nominatim(user_agent=str(uuid.uuid4()))
                location = locator.geocode(json.getaddress())
                object.point.setlon(location.longitude)
                object.point.setlat(location.latitude)
            else:
                object.point.setlon(json.getlongitude())
                object.point.setlat(json.getlatitude())
            DatabaseController().create_ActiveEmergency(object)
            return object

        # runs if emergency is off
        elif isinstance(json, EmergencyDelete):
            object.setuid(json.getuid())
            DatabaseController().remove_ActiveEmergency(query=f'uid = "{object.uid}"')
            object.settype('b-a-o-can')
            object.detail.emergency.setcancel('true')
            return object

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject
