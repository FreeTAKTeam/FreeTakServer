from FreeTAKServer.model.SpecificCoT.SendSimpleCoT import SendSimpleCoT
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.FTSModel.Event import Event as event
import json as jsonmodule
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendSimpleCoTController").getLogger()


class SendSimpleCoTController:
    def __init__(self, json):
        tempObject = event.SimpleCoT()
        object = SendSimpleCoT()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            object.sethow(json.gethow())
            ID = json.getattitude()
            a = RestEnumerations
            COTTYPE = json.getgeoObject()
            if "-.-" in COTTYPE:
                COTTYPE = COTTYPE.replace('a-.-', ID)
            else:
                raise Exception('geoObject not supported')
            object.settype(COTTYPE)
            point = object.point
            point.setlon(json.getlongitude())
            point.setlat(json.getlatitude())
            object.detail.contact.setcallsign(json.name)
            if json.gettimeout() != '':
                object.setstale(staletime=int(json.gettimeout()))
            else:
                object.setstale(staletime=RestAPIVariables.defaultGeoObjectTimeout)
            return object
        except AttributeError as e:
            raise Exception('a parameter has been passed which is not recognized with error: ' + str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject
