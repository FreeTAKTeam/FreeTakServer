from FreeTAKServer.model.SpecificCoT.SendGeoChat import SendGeoChat
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendGeoChatController").getLogger()

class SendChatController:
    def __init__(self, json):
        tempObject = event.GeoChat()
        object = SendGeoChat()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        object.detail.remarks.setINTAG(json.getmessage())
        object.detail.remarks.setsource(json.getsender())
        object.detail.link.setuid(json.getsender())
        return object

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject