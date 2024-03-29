from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.model.SpecificCoT.SendTakPong import SendTakPong

from .SendCoTAbstractController import SendCoTAbstractController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendInvalidCoTController").getLogger()
class SendPingController(SendCoTAbstractController):
    def __init__(self, RawCoT = None):
        try:
            RawCoT.xmlString = b'<event/>'
            tempObject = super().Event.takPong()
            object = SendTakPong()
            if RawCoT is not None:
                self.fill_object(object, tempObject, RawCoT, addToDB=False)
            else:
                pass
        except Exception as e:
            logger.error("there has been an exception in"
                         " the creation of a Ping model object " + str(e))
