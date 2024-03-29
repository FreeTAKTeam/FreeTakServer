from digitalpy.core.main.object_factory import ObjectFactory
import pathlib
from asyncio import Queue
import multiprocessing
import threading
from FreeTAKServer.core.services.Orchestrator import Orchestrator
from FreeTAKServer.core.connection.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.core.connection.ReceiveConnections import ReceiveConnections
from FreeTAKServer.core.connection.TCPSocketController import TCPSocketController
from FreeTAKServer.core.configuration.MainConfig import MainConfig
import os
from digitalpy.core.main.impl.default_factory import DefaultFactory
from digitalpy.core.digipy_configuration.impl.inifile_configuration import InifileConfiguration
from multiprocessing.pool import ThreadPool
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.persistence.DatabaseController import (
    DatabaseController,
)
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.Enumerations.connectionTypes import ConnectionTypes
from FreeTAKServer.model.TCPConnection import TCPConnection
from FreeTAKServer.model.SpecificCoT.Presence import Presence

loggingConstants = LoggingConstants(log_name="FTS-TCP_CoT_Service")
logger = CreateLoggerController(
    "FTS-TCP_CoT_Service", logging_constants=loggingConstants
).getLogger()


class TCPCoTServiceController(Orchestrator):
    def component_processed(self, data):
        return 1

    def __init__(self):
        super().__init__()

    @property
    def connection_type(self):
        return ConnectionTypes.TCP

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
            actionmapper.add_topic(
                f"/routing/response/{self.__class__.__name__.lower()}"
            )

            self.logger = logger
            self.dbController = DatabaseController()
            # self.clear_user_table()
            os.chdir("../../../")
            # create socket controller
            self.TCPSocketController = TCPSocketController()
            self.TCPSocketController.changeIP(IP)
            self.TCPSocketController.changePort(CoTPort)
            sock = self.TCPSocketController.createSocket()
            pool = ThreadPool(processes=2)
            self.pool = pool
            self.clientDataRecvPipe = clientDataRecvPipe
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
            )
        except Exception as e:
            logger.error(
                "there has been an exception in the start function "
                "of TCPCoTService " + str(e)
            )
            return e

    def add_service_user(self, clientInformation: ClientInformation):
        """this method generates the presence and connection objects from the
        clientInformation parameter and sends it to

        :param clientInformation: this is the information of the client to be added
        :return:
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():
                presence_object = Presence()
                presence_object.setModelObject(clientInformation.modelObject)

                # TODO why is this not xmlString?
                presence_object.setXmlString(clientInformation.idData)
                # Is this duplicate of modelObject?
                presence_object.setClientInformation(clientInformation.modelObject)

                connection_object = TCPConnection()
                connection_object.sock = None
                connection_object.user_id = clientInformation.modelObject.uid

                # Updating clientDataPipe
                # TODO add blocking...
                self.clientDataPipe.put(
                    ["add", presence_object, self.openSockets, connection_object]
                )
                self.logger.debug(
                    "client addition has been sent through queue "
                    + str(clientInformation)
                )
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as e:
            self.logger.error(
                "exception has been thrown adding client data from queue " + str(e)
            )
            raise e
