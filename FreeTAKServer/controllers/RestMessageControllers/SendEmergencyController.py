from FreeTAKServer.model.SpecificCoT.SendEmergency import SendEmergency
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.model.RestMessages.EmergencyPost import EmergencyPost, RestEnumerations
from FreeTAKServer.model.RestMessages.EmergencyDelete import EmergencyDelete
loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendGeoChatController").getLogger()


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
            object.point.setlat(json.getlatitude())
            object.point.setlon(json.getlongitude())
            DatabaseController().create_ActiveEmergency(object)
            return object

        # runs if emergency is off
        elif isinstance(json, EmergencyDelete):
            object.setuid(json.getuid())
            DatabaseController().remove_ActiveEmergency(query=f'uid == "{object.uid}"')
            object.settype('b-a-o-can')
            object.detail.emergency.setcancel('true')
            return object

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject


if __name__ == "__main__":
    SendEmergencyController('{"name": "test", "emergencyType": "911 Alert", "status": "on"}')
    SendEmergencyController('{"uid": "d7f30cf5-1d4d-11eb-b036-2cf05d092d98", "status": "off"}')
