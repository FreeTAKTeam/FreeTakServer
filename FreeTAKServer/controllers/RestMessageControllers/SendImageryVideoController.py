from FreeTAKServer.model.SpecificCoT.SendImageryVideo import SendImageryVideo
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.controllers.parsers.XMLCoTController import XMLCoTController

class SendImageryVideoController:
    def __init__(self, json):
        tempObject = event.BitsImageryVideo()
        object = SendImageryVideo()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        from urllib.parse import urlparse
        url = json.geturl()
        url = urlparse(url)

        name = json.getname()

        object.detail.contact.setcallsign(name)
        object.detail._video.ConnectionEntry.setuid(object.getuid())
        object.detail._video.ConnectionEntry.setpath(url.path)
        object.detail._video.ConnectionEntry.setaddress(url.netloc.split(":")[0])
        object.detail._video.ConnectionEntry.setport(url.netloc.split(":")[1])
        object.detail._video.ConnectionEntry.setprotocol(url.scheme)
        object.detail._video.ConnectionEntry.setalias(name)
        return object

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject