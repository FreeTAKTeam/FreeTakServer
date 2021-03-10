from FreeTAKServer.controllers.services.Orchestrator import Orchestrator
from FreeTAKServer.controllers.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.controllers.ReceiveConnections import ReceiveConnections
import os
from FreeTAKServer.controllers.SSLSocketController import SSLSocketController
from multiprocessing.pool import ThreadPool
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("FTS").getLogger()

class SSLCoTServiceController(Orchestrator):
    def start(self, IP, CoTPort, Event, clientDataPipe, ReceiveConnectionKillSwitch, RestAPIPipe):
        try:
            import selectors
            self.dbController = DatabaseController()
            print('ssl cot service starting')
            os.chdir('../../')
            # create socket controller
            self.SSLSocketController = SSLSocketController()
            self.SSLSocketController.changeIP(IP)
            self.SSLSocketController.changePort(CoTPort)
            sock = self.SSLSocketController.createSocket()
            sock.listen()
            self.sel = self._create_selector()
            self.sel.register(sock, selectors.EVENT_READ, data=None)
            # instantiate domain model and save process as object
            self.mainRunFunction(None, None, sock, None, Event, clientDataPipe,
                                 ReceiveConnectionKillSwitch, RestAPIPipe, True)
        except Exception as e:
            logger.error("there has been an exception thrown in"
                         " the starting of the ssl service " + str(e))
            return e