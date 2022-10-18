from digitalpy.core.object_factory import ObjectFactory
from FreeTAKServer.controllers.services.Orchestrator import Orchestrator
from FreeTAKServer.controllers.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.controllers.ReceiveConnections import ReceiveConnections
import os
from FreeTAKServer.controllers.SSLSocketController import SSLSocketController
from multiprocessing.pool import ThreadPool
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import (
    DatabaseController,
)

loggingConstants = LoggingConstants(log_name="FTS-SSL_CoT_Service")
logger = CreateLoggerController(
    "FTS-SSL_CoT_Service", logging_constants=loggingConstants
).getLogger()


class SSLCoTServiceController(Orchestrator):
    def start(
        self,
        IP,
        CoTPort,
        Event,
        clientDataPipe,
        ReceiveConnectionKillSwitch,
        RestAPIPipe,
        clientDataRecvPipe,
        factory,
    ):
        try:
            # configure the object factory with the passed factory instance
            ObjectFactory.configure(factory)
            actionmapper = ObjectFactory.get_instance("actionMapper")
            # subscribe to responses originating from this controller
            actionmapper.add_topic(f"/routing/response/{self.__class__.__name__}")

            self.logger = logger
            self.dbController = DatabaseController()
            print("ssl cot service starting")
            os.chdir("../../")
            # create socket controller
            self.SSLSocketController = SSLSocketController()
            self.SSLSocketController.changeIP(IP)
            self.SSLSocketController.changePort(CoTPort)
            sock = self.SSLSocketController.createSocket()
            # threadpool is used as it allows the transfer of SSL socket unlike processes
            pool = ThreadPool(processes=2)
            self.clientDataRecvPipe = clientDataRecvPipe
            self.pool = pool
            clientData = pool.apply_async(
                ClientReceptionHandler().startup, (self.clientInformationQueue,)
            )
            receiveConnection = pool.apply_async(ReceiveConnections().listen, (sock,))
            # instantiate domain model and save process as object
            self.mainRunFunction(
                clientData,
                receiveConnection,
                sock,
                pool,
                Event,
                clientDataPipe,
                ReceiveConnectionKillSwitch,
                RestAPIPipe,
                True,
            )
        except Exception as e:
            print(e)
            logger.error(
                "there has been an exception thrown in"
                " the starting of the ssl service " + str(e)
            )
            return e
