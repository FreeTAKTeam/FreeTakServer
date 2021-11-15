from FreeTAKServer.model.SpecificCoT.SendRoute import SendRoute
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
import uuid
from FreeTAKServer.model.FTSModel.Event import Event as event
import json as jsonmodule
from lxml.etree import tostring
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables
from geopy import Nominatim
loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendSimpleCoTController").getLogger()

class SendRouteController:
    def __init__(self, json):
        tempObject = event.Route()
        # tempObject.detail.setlink(None)
        # tempObject.detail.setlink(None)
        object = SendRoute()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        object.setXmlString(tostring(XmlSerializer().from_fts_object_to_format(object.modelObject)))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object: event, json):
        try:
            point = object.point
            end = object.detail.getlink()
            if json.getaddress():
                locator = Nominatim(user_agent=str(uuid.uuid4()))
                location = locator.geocode(json.getaddress())
                end.setpoint(f"{location.latitude}, {location.longitude}")
                # point.setlat(location.latitude)
            else:
                end.setpoint(f"{json.getlatitudeDest()}, {json.getlongitudeDest()}")
            end.setcallsign(json.getendName())
            object.detail.setlink(end)
            object.detail.contact.setcallsign(json.getrouteName())
            object.detail.link_attr.setmethod(json.getmethod)
            start = object.detail.getlink()
            start.setpoint(f"{json.getlatitude()}, {json.getlongitude()}")
            start.setcallsign(json.getstartName())
            object.detail.setlink(start)
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