from digitalpy.core.object_factory import ObjectFactory
from FreeTAKServer.controllers.services.Orchestrator import Orchestrator
from FreeTAKServer.controllers.connection.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.controllers.connection.ReceiveConnections import ReceiveConnections
import os
from FreeTAKServer.controllers.connection.SSLSocketController import SSLSocketController
from multiprocessing.pool import ThreadPool
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.persistence.DatabaseController import (
    DatabaseController,
)
from FreeTAKServer.model.Enumerations.connectionTypes import ConnectionTypes
from FreeTAKServer.model.SSLConnection import SSLConnection
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.SpecificCoT.Presence import Presence

loggingConstants = LoggingConstants(log_name="FTS-SSL_CoT_Service")
logger = CreateLoggerController(
    "FTS-SSL_CoT_Service", logging_constants=loggingConstants
).getLogger()


class SSLCoTServiceController(Orchestrator):
    @property
    def connection_type(self):
        return ConnectionTypes.SSL

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

    def add_service_user(self, client_information: ClientInformation):
        """this method generates the presence and connection objects from the
        client_information parameter and sends it to the clientDataPipe for processing

        :param client_information: this is the information of the client to be added
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():
                presence_object = Presence()
                presence_object.setModelObject(client_information.modelObject)

                # TODO why is this not xmlString?
                presence_object.setXmlString(client_information.idData)
                # is this duplicate of modelobject ?
                presence_object.setClientInformation(client_information.modelObject)

                connection_object = SSLConnection()
                # TODO: add certificate name derived from socket
                connection_object.certificate_name = None
                connection_object.sock = None
                connection_object.user_id = client_information.modelObject.uid

                # Updating clientDataPipe
                # TODO add blocking...
                self.clientDataPipe.put(
                    ["add", presence_object, self.openSockets, connection_object]
                )
                self.logger.debug(
                    "client addition has been sent through queue "
                    + str(client_information)
                )
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as e:
            self.logger.error(
                "exception has been thrown adding client data from queue " + str(e)
            )
            raise e
