from FreeTAKServer.controllers.services.Orchestrator import Orchestrator
from FreeTAKServer.controllers.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.controllers.ReceiveConnections import ReceiveConnections
from FreeTAKServer.controllers.TCPSocketController import TCPSocketController
import os
from multiprocessing.pool import ThreadPool
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
loggingConstants = LoggingConstants()
logger = CreateLoggerController("FTS").getLogger()

class TCPCoTServiceController(Orchestrator):
    def start(self, IP, CoTPort, Event, clientDataPipe, ReceiveConnectionKillSwitch, RestAPIPipe):
        try:
            self.dbController = DatabaseController()
            clientDataPipe.send(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><event version="2.0" uid="ANDROID-359975090666199" type="a-f-G-U-C" time="2020-08-23T19:02:10.317Z" start="2020-08-23T19:02:10.317Z" stale="2020-08-23T19:08:25.317Z" how="m-g"><point lat="43.855695" lon="-66.108013" hae="28.2586566130189" ce="3.2" le="9999999.0"/><detail><takv os="28" version="4.0.0.1 (3a23eb4e).1585690033-CIV" device="SAMSUNG SM-G950W" platform="ATAK-CIV"/><contact endpoint="*:-1:stcp" phone="19027743142" callsign="NOVA"/><uid Droid="NOVA"/><precisionlocation altsrc="GPS" geopointsrc="GPS"/><__group role="Team Member" name="Yellow"/><status battery="35"/><track course="255.63907109587313" speed="0.0"/></detail></event>')

            os.chdir('../../../')
            # create socket controller
            self.TCPSocketController = TCPSocketController()
            self.TCPSocketController.changeIP(IP)
            self.TCPSocketController.changePort(CoTPort)
            sock = self.TCPSocketController.createSocket()
            pool = ThreadPool(processes=2)
            self.pool = pool
            clientData = pool.apply_async(ClientReceptionHandler().startup, (self.clientInformationQueue,))
            receiveConnection = pool.apply_async(ReceiveConnections().listen, (sock,))
            # instantiate domain model and save process as object
            self.mainRunFunction(clientData, receiveConnection, sock, pool, Event, clientDataPipe,
                                 ReceiveConnectionKillSwitch, RestAPIPipe)
        except Exception as e:
            logger.error('there has been an exception in the start function '
                         'of TCPCoTService ' + str(e))
            return e
