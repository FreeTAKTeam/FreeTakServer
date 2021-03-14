from FreeTAKServer.model.SpecificCoT.SendGeoChat import SendGeoChat
from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendGeoChatController").getLogger()

class SendGeoChatController(SendCoTAbstractController):
    def __init__(self, RawCoT=None):
        try:
            tempObject = super().Event.GeoChat()
            object = SendGeoChat()
            if RawCoT is not None:
                self.fill_object(object, tempObject, RawCoT)
            else:
                pass
        except Exception as e:
            logger.error("there has been an exception in the creation"
                         " of the send Geo Chat object " + str(e))
            return -1