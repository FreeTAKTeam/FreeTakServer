from FreeTAKServer.model.SpecificCoT.SendSensorDrone import SendSensorDrone
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.model.FTSModel.Event import Event as event
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController

class SendSensorDroneController:
    def __init__(self, json):
        tempObject = event.DroneSensor()
        object = SendSensorDrone()
        object.setModelObject(tempObject)
        object.modelObject = self._serializeJsonToModel(object.modelObject, json)
        # commented in version 1.9.1, reduces average endpoint time by a factor of 10
        #DatabaseController().create_CoT(object.modelObject)
        object.setXmlString(XMLCoTController().serialize_model_to_CoT(object.modelObject))
        self.setCoTObject(object)

    def _serializeJsonToModel(self, object, json):
        if json.gettimeout():
            object.setstale(staletime=json.gettimeout())
        if json.getuid():
            object.setuid(json.getuid())
        if json.getlatitude():
            object.point.setlon(json.getlongitude())
        if json.getlatitude():
            object.point.setlat(json.getlatitude())
        if json.getname():
            object.detail.contact.setcallsign(json.getname())
        if json.getFieldOfView():
            object.detail.sensor.setfov(json.getFieldOfView())
        if json.getRange():
            object.detail.sensor.setrange(json.getRange())
        if json.getBearing():
            object.detail.track.setcourse(json.getBearing())
        if json.getBearing():
            object.detail.sensor.setazimuth(json.getBearing())
        if json.getVideoURLUID():
            object.detail._video.seturl(json.getVideoURLUID())
        return object

    def setCoTObject(self, CoTObject):
        self.CoTObject = CoTObject

    def getCoTObject(self):
        return self.CoTObject