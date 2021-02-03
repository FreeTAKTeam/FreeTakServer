from FreeTAKServer.model.SpecificCoT.SendChecklist import SendChecklist
from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendChecklistController").getLogger()


class SendChecklistController(SendCoTAbstractController):
    def __init__(self, RawCoT):
        try:
            tempObject = super().Event.disconnect()
            object = SendChecklist()
            self.fill_object(object, tempObject, RawCoT, addToDB=False)
        except Exception as e:
            logger.error("there has been an exception in the creation of the send Checklist object " + str(e))
            return -1
