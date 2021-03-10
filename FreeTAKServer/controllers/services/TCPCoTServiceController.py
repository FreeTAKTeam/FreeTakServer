from FreeTAKServer.controllers.services.Orchestrator import Orchestrator
from FreeTAKServer.controllers.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.controllers.ReceiveConnections import ReceiveConnections
from FreeTAKServer.controllers.TCPSocketController import TCPSocketController
import os
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("FTS").getLogger()

class TCPCoTServiceController(Orchestrator):

    def start(self, IP, CoTPort, Event, clientDataPipe, ReceiveConnectionKillSwitch, RestAPIPipe):
        try:
            print("running start")
            import selectors
            self.dbController = DatabaseController()
            # self.clear_user_table()
            os.chdir('../../../')
            # create socket controller
            self.TCPSocketController = TCPSocketController()
            self.TCPSocketController.changeIP(IP)
            self.TCPSocketController.changePort(CoTPort)
            sock = self.TCPSocketController.createSocket()
            sock.listen()
            print("socket created now registering")
            self.sel = self._create_selector()
            self.sel.register(sock, selectors.EVENT_READ, data=None)
            # instantiate domain model and save process as object
            self.mainRunFunction(None, None, sock, None, Event, clientDataPipe,
                                 ReceiveConnectionKillSwitch, RestAPIPipe)
        except Exception as e:
            logger.error('there has been an exception in the start function '
                         'of TCPCoTService ' + str(e))
            return e
