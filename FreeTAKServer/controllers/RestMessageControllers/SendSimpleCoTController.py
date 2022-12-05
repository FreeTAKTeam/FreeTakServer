import uuid

from defusedxml import ElementTree as etree
from FreeTAKServer.controllers.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.model.SpecificCoT.SendSimpleCoT import SendSimpleCoT
from geopy import Nominatim

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendSimpleCoTController").getLogger()

class SendSimpleCoTController:
    def __init__(self, json):
        tempObject = event.SimpleCoT()
        object = SendSimpleCoT()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        DatabaseController().create_CoT(object.modelObject)
        object.setXmlString(etree.tostring(XmlSerializer().from_fts_object_to_format(object.modelObject)))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            if json.getuid():
                object.setuid(json.getuid())
            object.sethow(json.gethow())
            COTTYPE = json.getgeoObject()
            if "-.-" in COTTYPE:
                ID = json.getattitude()
                COTTYPE = COTTYPE.replace('-.-', ID)
            else:
                pass
            object.settype(COTTYPE)
            point = object.point
            if json.getaddress():
                locator = Nominatim(user_agent=str(uuid.uuid4()))
                location = locator.geocode(json.getaddress())
                point.setlon(location.longitude)
                point.setlat(location.latitude)
            else:
                point.setlon(json.getlongitude())
                point.setlat(json.getlatitude())
            object.detail.contact.setcallsign(json.name)
            if json.gettimeout() != '':
                object.setstale(staletime=int(json.gettimeout()))
            else:
                object.setstale(staletime=RestAPIVariables.defaultGeoObjectTimeout)
            return object
        except AttributeError as e:
            raise Exception('a parameter has been passed which is not recognized with error: '+str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject

class UpdateSimpleCoTController:
    def __init__(self, json):
        tempObject = event.SimpleCoT()
        object = SendSimpleCoT()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        DatabaseController().create_CoT(object.modelObject)
        object.setXmlString(etree.tostring(XmlSerializer().from_fts_object_to_format(object.modelObject)))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            object.setuid(json.getuid())
            object.sethow(json.gethow())
            COTTYPE = json.getgeoObject()
            if "-.-" in COTTYPE:
                ID = json.getattitude()
                COTTYPE = COTTYPE.replace('-.-', ID)
            else:
                pass
            object.settype(COTTYPE)
            point = object.point
            if json.getaddress():
                locator = Nominatim(user_agent=str(uuid.uuid4()))
                location = locator.geocode(json.getaddress())
                point.setlon(location.longitude)
                point.setlat(location.latitude)
            else:
                point.setlon(json.getlongitude())
                point.setlat(json.getlatitude())
            object.detail.contact.setcallsign(json.name)
            if json.gettimeout() != '':
                object.setstale(staletime=int(json.gettimeout()))
            else:
                object.setstale(staletime=RestAPIVariables.defaultGeoObjectTimeout)
            return object
        except AttributeError as e:
            raise Exception('a parameter has been passed which is not recognized with error: '+str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject
