from FreeTAKServer.model.SpecificCoT.SendVideoStream import SendVideoStream
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.FTSModel.Event import Event as event
import json as jsonmodule
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.core.configuration.RestAPIVariables import RestAPIVariables
from geopy import Nominatim
from defusedxml import ElementTree as etree
from FreeTAKServer.core.persistence.DatabaseController import DatabaseController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendSimpleCoTController").getLogger()

class SendVideoStreamController:
    def __init__(self, json):
        tempObject = event.VideoStream()
        object = SendVideoStream()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        DatabaseController().create_CoT(object.modelObject)
        object.setXmlString(etree.tostring(XmlSerializer().from_fts_object_to_format(object.modelObject)))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            object.detail._video.ConnectionEntry.setaddress(json["streamAddress"])
            object.detail._video.ConnectionEntry.setalias(json["alias"])
            object.detail.contact.setcallsign(json["alias"])
            object.detail._video.ConnectionEntry.setpath(json["streamPath"])
            object.detail._video.ConnectionEntry.setport(json["streamPort"])
            object.detail._video.ConnectionEntry.setprotocol(json["streamProtocol"])
            object.detail._video.seturl(json["streamAddress"]+":"+json["streamPort"]+json["streamPath"])
            del object.detail.marti
            object.getuid()
            object.detail._video.ConnectionEntry.setuid(object.getuid())
            object.detail.link.setuid(object.getuid())
            return object
        except AttributeError as e:
            raise Exception('a parameter has been passed which is not recognized with error: '+str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject