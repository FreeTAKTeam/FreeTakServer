from asyncio import Queue
import multiprocessing
import threading
from FreeTAKServer.controllers.services.Orchestrator import Orchestrator
from FreeTAKServer.controllers.ClientReceptionHandler import ClientReceptionHandler
from FreeTAKServer.controllers.ReceiveConnections import ReceiveConnections
from FreeTAKServer.controllers.TCPSocketController import TCPSocketController
import os
from multiprocessing.pool import ThreadPool
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.controllers.CreateLoggerController import CreateLoggerController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.model.Enumerations.connectionTypes import ConnectionTypes
from FreeTAKServer.model.TCPConnection import TCPConnection
from FreeTAKServer.model.SpecificCoT.Presence import Presence

loggingConstants = LoggingConstants(log_name="FTS-TCP_CoT_Service")
logger = CreateLoggerController("FTS-TCP_CoT_Service", logging_constants=loggingConstants).getLogger()

class TCPCoTServiceController(Orchestrator):
    def __init__(self):
        # TODO add proper instantiation
        pass

    @property
    def connection_type(self):
        return ConnectionTypes.TCP

    def start(self, IP, CoTPort, Event, clientDataPipe, ReceiveConnectionKillSwitch, RestAPIPipe, clientDataRecvPipe):
        try:
            self.logger = logger
            self.dbController = DatabaseController()
            # self.clear_user_table()
            os.chdir('../../../')
            # create socket controller
            self.TCPSocketController = TCPSocketController()
            self.TCPSocketController.changeIP(IP)
            self.TCPSocketController.changePort(CoTPort)
            sock = self.TCPSocketController.createSocket()
            pool = ThreadPool(processes=2)
            self.pool = pool
            self.clientDataRecvPipe = clientDataRecvPipe
            clientData = pool.apply_async(ClientReceptionHandler().startup, (self.clientInformationQueue,))
            receiveConnection = pool.apply_async(ReceiveConnections().listen, (sock,))
            # instantiate domain model and save process as object
            self.mainRunFunction(clientData, receiveConnection, sock, pool, Event, clientDataPipe,
                                 ReceiveConnectionKillSwitch, RestAPIPipe)
        except Exception as e:
            logger.error('there has been an exception in the start function '
                         'of TCPCoTService ' + str(e))
            return e

    def add_service_user(self, client_information: ClientInformation):
        """ this method generates the presence and connection objects from the
        client_information parameter and sends it to

        :param client_information: this is the information of the client to be added
        :return:
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():
                presence_object = Presence()
                presence_object.setModelObject(client_information.modelObject)

                # TODO why is this not xmlString?
                presence_object.setXmlString(client_information.idData)
                # Is this duplicate of modelObject?
                presence_object.setClientInformation(client_information.modelObject)

                connection_object = TCPConnection()
                connection_object.sock = None
                connection_object.user_id = client_information.modelObject.uid

                # Updating clientDataPipe
                # TODO add blocking...
                self.clientDataPipe.put(['add', presence_object, self.openSockets, self.connection_object])
                self.logger.debug("client addition has been sent through queue " + str(client_information))
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as e:
            self.logger.error("exception has been thrown adding client data from queue " + str(e))
            raise e


    def mainRunFunction(
            self,
            clientData,
            receiveConnection,
            sock,
            pool,
            event,
            clientDataPipe: Queue,
            ReceiveConnectionKillSwitch,
            CoTSharePipe,
            ssl=False):
        """ This is the central method which is responsable for the functioning of the CoT service's it iterates over
        two main sub services,
        ReceiveConnections, which receives new connections to the server,
        ClientReceptionHandler, which receives data from connected clients,

        for each of these methods the respective data handlers are called and the serialization process begins

        :param clientData:
        :param receiveConnection: Connection information
        :param sock:
        :param pool:
        :param event:
        :param clientDataPipe:
        :param ReceiveConnectionKillSwitch: Event object that holds a is_set flag
        :param CoTSharePipe:
        :param ssl:
        """
        self.logger.debug('Server started...')

        # TODO move to ConnectionMonitorController
        threading.Thread(target=self.monitor).start()
        # TODO remove
        self.ssl = ssl

        import datetime
        import time

        start_timer = time.time() - 60

        while event.is_set():
            self.CoTSharePipe = CoTSharePipe

            try:
                self.clientDataPipe = clientDataPipe

                if not event.is_set():
                    self.stop()
                    break

                try:
                    # Flag initially set to false
                    if ReceiveConnectionKillSwitch.is_set():
                        try:
                            # Check if ReceiveConnection was successful 
                            receiveConnection.successful()
                            ReceiveConnectionKillSwitch.clear()
                            receiveConnection = pool.apply_async(ReceiveConnections().listen, (sock,))
                        except ValueError as e:
                            logger.error(f'Error in receive connection listening: {e}')
                    else:
                        self.logger.debug('Receiving new connection...')
                        receiveConnectionOutput = receiveConnection.get(timeout=0.01)
                        self.connection_received += 1
                        self.logger.debug(f'Connection received. Total connections {self.connection_received}')
                        receiveConnection = pool.apply_async(ReceiveConnections().listen, (sock, ssl,))
                        self.handel_connection_data(receiveConnectionOutput)

                except Exception as e:
                    self.logger.error('exception in receive connection within main run function ' + str(e))

                try:
                    # attempt to retrieve data from the client reception handler
                    clientDataOutput = clientData.get(timeout=0.01)

                    if self.checkOutput(clientDataOutput) and isinstance(clientDataOutput, list):
                        if clientDataOutput != []:
                            # just added so log exist of most recent client data output and the time it was sent
                            recent_client_data_output = (clientDataOutput, time.time())

                        # add the length of this list to the number of received messages
                        self.received_message_count += len(clientDataOutput)
                        self.handel_regular_data(clientDataOutput)
                    else:
                        raise Exception(f'Client reception handler has returned data which is not of type list data is {clientDataOutput}')
                    self.get_client_information()
                    clientData = pool.apply_async(ClientReceptionHandler().startup, (self.clientInformationQueue,))
                except Exception as e:
                    self.logger.info('exception in receive client data within main run function ' + str(e))
                try:
                    for x in range(100):
                        if not CoTSharePipe.empty():

                            data = CoTSharePipe.get()
                            self.handel_shared_data(data)
                        else:
                            break
                except Exception as e:
                    self.logger.error(
                        'there has been an excepion in the handling of data supplied by the rest API ' + str(e))

                try:
                    if time.time() > start_timer + 60:
                        start_timer = time.time()
                        self.logger.debug('mainRunFunction is running')

                        if 'recent_client_data_output' in locals():
                            self.logger.debug('most recent client data ' + str(recent_client_data_output))
                            self.logger.debug(
                                'time since last valid data ' + str(time.time() - recent_client_data_output[1]))
                            self.logger.debug(
                                'content of last valid data ' + str(recent_client_data_output[0][0].xmlString))
                        self.logger.debug('client dict: ' + str(self.clientInformationQueue))
                except Exception as e:
                    self.logger.error("the periodic debug message has thrown an error " + str(e))
            except Exception as e:
                self.logger.info('there has been an uncaught error thrown in mainRunFunction' + str(e))
        self.stop()
