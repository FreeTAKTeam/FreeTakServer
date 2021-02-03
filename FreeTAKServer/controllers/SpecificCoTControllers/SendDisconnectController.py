from FreeTAKServer.model.SpecificCoT.SendDisconnect import SendDisconnect
from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendDisconnectController").getLogger()


class SendDisconnectController(SendCoTAbstractController):
    def __init__(self, RawCoT):
        try:
            tempObject = super().Event.disconnect()
            object = SendDisconnect()
            self.fill_object(object, tempObject, RawCoT, addToDB=False)
        except Exception as e:
            logger.error("there has been an exception in the creation of the send disconnect object " + str(e))
            return -1
