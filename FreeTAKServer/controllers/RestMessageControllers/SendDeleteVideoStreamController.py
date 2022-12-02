from FreeTAKServer.model.SpecificCoT.SendDeleteVideoStream import SendDeleteVideoStream
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.FTSModel.Event import Event as event
import json as jsonmodule
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from FreeTAKServer.controllers.configuration.RestAPIVariables import RestAPIVariables
from defusedxml import ElementTree as etree
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendDeleteVideoStreamController").getLogger()

class SendDeleteVideoStreamController:
    def __init__(self, json):
        tempObject = event.DeleteVideo()
        object = SendDeleteVideoStream()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        DatabaseController().create_CoT(object.modelObject)
        object.setXmlString(etree.tostring(XmlSerializer().from_fts_object_to_format(object.modelObject)))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        try:
            json.getuid()
            object.setuid(json.getuid())
            object.detail.link.setuid(json.getuid())
            return object
        except AttributeError as e:
            raise Exception('a parameter has been passed which is not recognized with error: '+str(e))

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject