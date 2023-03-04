from FreeTAKServer.model.SpecificCoT.Presence import Presence
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.FTSModel.Event import Event as event
import json as jsonmodule
from FreeTAKServer.core.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.core.configuration.RestAPIVariables import RestAPIVariables
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendPresenceController").getLogger()

class UpdatePresenceController:
    def __init__(self, json):
        tempObject = event.Presence()
        object = Presence()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        DatabaseController().create_CoT(object.modelObject)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            object.setuid(json.getuid())
            object.sethow(json.gethow())
            object.type = RestAPIVariables.defaultPresenceType
            point = object.point
            point.setlon(json.getlongitude())
            point.setlat(json.getlatitude())
            object.detail.contact.setcallsign(json.getname())
            object.detail._group.setname(json.getteam())
            object.detail._group.setrole(json.getrole())
            object.detail.remarks.setINTAG(json.getremarks())
            if json.gettimeout() != '':
                object.setstale(staletime=int(json.gettimeout()))
            else:
                object.setstale(staletime=RestAPIVariables.defaultPresenceTimeout)
            return object
        except AttributeError as e:
            return Exception('a parameter has been passed which is not recognized with error: '+str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject


class SendPresenceController:
    def __init__(self, json):
        tempObject = event.Presence()
        object = Presence()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        DatabaseController().create_CoT(object.modelObject)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            if json.getuid():
                object.setuid(json.getuid())
            object.sethow(json.gethow())
            object.type = RestAPIVariables.defaultPresenceType
            point = object.point
            point.setlon(json.getlongitude())
            point.setlat(json.getlatitude())
            object.detail.contact.setcallsign(json.getname())
            object.detail._group.setname(json.getteam())
            object.detail._group.setrole(json.getrole())
            object.detail.remarks.setINTAG(json.getremarks())
            if json.gettimeout() != '':
                object.setstale(staletime=int(json.gettimeout()))
            else:
                object.setstale(staletime=RestAPIVariables.defaultPresenceTimeout)
            return object
        except AttributeError as e:
            return Exception('a parameter has been passed which is not recognized with error: '+str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject