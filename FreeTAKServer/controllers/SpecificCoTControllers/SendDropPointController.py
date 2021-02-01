from FreeTAKServer.model.SpecificCoT.SendDropPoint import SendDropPoint
from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendDropPointController").getLogger()

class SendDropPointController(SendCoTAbstractController):
    def __init__(self, RawCoT=None):
        try:
            tempObject = super().Event.dropPoint()
            object = SendDropPoint()
            if RawCoT is not None:
                self.fill_object(object, tempObject, RawCoT)
            else:
                pass
        except Exception as e:
            logger.error("there has been an exception in the creation of the send drop point object " + str(e))
            return -1