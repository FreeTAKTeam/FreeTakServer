from FreeTAKServer.model.SpecificCoT.SendExcheckUpdate import SendExcheckUpdate
from .SendCoTAbstractController import SendCoTAbstractController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.configuration.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants()
logger = CreateLoggerController("SendExcheckUpdateController").getLogger()

class SendExcheckUpdateController(SendCoTAbstractController):
    def __init__(self, RawCoT):
        try:
            tempObject = super().Event.ExcheckUpdate()
            object = SendExcheckUpdate()
            self.fill_object(object, tempObject, RawCoT, addToDB=False)
        except Exception as e:
            logger.error("there has been an exception in the creation of the send Emergency object " + str(e))