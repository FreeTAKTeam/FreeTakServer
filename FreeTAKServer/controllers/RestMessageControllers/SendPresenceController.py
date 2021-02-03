from FreeTAKServer.model.SpecificCoT.SendPrecense import SendPresence
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendPresenceController").getLogger()


class SendPresenceController:
    def __init__(self, json):
        tempObject = event.Presence()
        object = SendPresence()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            object.sethow(json.gethow())
            object.type = RestAPIVariables.defaultPresenceType
            point = object.point
            point.setlon(json.getlongitude())
            point.setlat(json.getlatitude())
            object.detail.contact.setcallsign(json.getname())
            object.detail._group.setname(json.getteam())
            object.detail._group.setrole(json.getrole())
            if json.gettimeout() != '':
                object.setstale(staletime=int(json.gettimeout()))
            else:
                object.setstale(staletime=RestAPIVariables.defaultPresenceTimeout)
            return object
        except AttributeError as e:
            return Exception('a parameter has been passed which is not recognized with error: ' + str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject
