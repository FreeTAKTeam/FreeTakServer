from FreeTAKServer.core.configuration.CreateLoggerController import \
    CreateLoggerController
from FreeTAKServer.core.configuration.LoggingConstants import \
    LoggingConstants
from FreeTAKServer.model.SpecificCoT.SendGeoChat import SendGeoChat

from .SendCoTAbstractController import SendCoTAbstractController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendGeoChatController").getLogger()

class SendGeoChatController(SendCoTAbstractController):
    def __init__(self, RawCoT=None, AddToDB = True):
        try:
            tempObject = super().Event.GeoChat()
            object = SendGeoChat()
            if RawCoT is not None:
                self.fill_object(object, tempObject, RawCoT, addToDB= AddToDB)
            else:
                pass
        except Exception as e:
            logger.error("there has been an exception in the creation"
                         " of the send Geo Chat object " + str(e))
