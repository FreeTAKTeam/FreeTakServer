#######################################################
# 
# orchestrator.py
# Python implementation of the Class orchestrator
# Generated by Enterprise Architect
# Created on:      21-May-2020 12:24:48 PM
# Original author: Natha Paquette
# 
#######################################################
from abc import ABC, abstractmethod
from asyncio import Queue
import threading
import time
import traceback

from FreeTAKServer.controllers.ActiveThreadsController import ActiveThreadsController
from FreeTAKServer.controllers.ClientInformationController import ClientInformationController
from FreeTAKServer.controllers.DatabaseControllers.DatabaseController import DatabaseController
from FreeTAKServer.controllers.ReceiveConnections import ReceiveConnections
from FreeTAKServer.controllers.ReceiveConnectionsProcessController import ReceiveConnectionsProcessController
from FreeTAKServer.controllers.SendDataController import SendDataController
from FreeTAKServer.controllers.SpecificCoTControllers.SendDisconnectController import SendDisconnectController
from FreeTAKServer.controllers.XMLCoTController import XMLCoTController
from FreeTAKServer.controllers.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.controllers.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.SpecificCoT.Presence import Presence
from FreeTAKServer.model.User import User
from FreeTAKServer.model.ClientInformation import ClientInformation

import multiprocessing
import importlib
import socket

loggingConstants = LoggingConstants()

from FreeTAKServer.controllers.ClientReceptionHandler import ClientReceptionHandler

# MAJOR TODO: Make explicit exception classes!!!

class Orchestrator(ABC):
    """ this class is the main class responsible for handling the CoT listener for XML
    """
    # TODO: fix repeat attempts to add user
    def __init__(self):
        self.logger = None

        # Server info
        self.connection_received = 0
        self.sent_message_count = 0
        self.received_message_count = 0
        self.messages_to_core_count = 0
        self.messages_from_core_count = 0
        self.openSockets = 0

        # Contains info on clients
        self.clientInformationQueue = {}
        self.clientDataPipe = Queue()

        # instantiate controllers
        self.ActiveThreadsController = ActiveThreadsController()
        self.ClientInformationController = ClientInformationController()
        self.ReceiveConnections = ReceiveConnections()
        self.ReceiveConnectionsProcessController = ReceiveConnectionsProcessController()
        self.XMLCoTController = XMLCoTController()
        self.dbController = DatabaseController()

    @property
    @abstractmethod
    def connection_type(self):
        """Implement as property
        """
        pass

    def remove_service_user(self, client_information: ClientInformation):
        """ Generates the presence object from the
        client_information parameter and sends it as a remove message
        to the client data pipe

        Args:
            client_information: Client information

        Returns: None
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():

                # Process removal of client in clientDataPipe
                # TODO add blocking
                self.clientDataPipe.put(['remove', client_information, self.openSockets, self.connection_type])
                self.logger.debug(f"Client removal has been sent through queue {str(client_information)}")
            else:
                self.logger.critical("Client data pipe is full!")
        except Exception as e:
            self.logger.error(f"Exception has been thrown removing client data from queue: {str(e)}")
            raise e

    def update_client_information(self, client_information: ClientInformation):
        """ Generates a Presence object from the client_information parameter and
        sends it as an update message to the client data pipe.

        :param client_information: Client information

        Returns: None
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():
                presence_object = Presence()
                presence_object.setModelObject(client_information.modelObject)
                presence_object.setXmlString(client_information.xmlString.decode())
                presence_object.setClientInformation(client_information.modelObject)

                # TODO add blocking
                self.clientDataPipe.put(['update', presence_object, self.openSockets, None])
                self.logger.debug("client update has been sent through queue " + str(client_information))

                self.get_client_information()
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as e:
            self.logger.error("exception has been thrown updating client data in queue "+str(e))
            raise e

    @abstractmethod
    def add_service_user(self, client_information: ClientInformation):
        """ Generates the presence and connection objects from the
        client_information parameter and sends it to the clientDataPipe for processing

        :param client_information: this is the information of the client to be added
        """
        pass

    def get_client_information(self):
        """ this method gets client information from the client information pipe and returns it as a dict merged
        with the current client information list and updates the self variable

        :return:
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():
                import copy

                # TODO implement blocking...
                self.clientDataPipe.put(["get", self.connection_type, self.openSockets])
                user_dict = self.clientDataRecvPipe.get(timeout=10000)
                client_information_queue_client_ids = copy.copy(list(self.clientInformationQueue.keys()))

                for client_id in client_information_queue_client_ids:
                    # forces FTS core to be single source of truth
                    if client_id in user_dict.keys() and len(self.clientInformationQueue[client_id]) == 1:
                        self.clientInformationQueue[client_id].append(user_dict[client_id])

                    elif client_id in user_dict.keys() and len(self.clientInformationQueue[client_id]) == 2:
                        self.clientInformationQueue[client_id][1] = user_dict[client_id]

                    # if the entry isn't present in FTS core than the client will be disconnected
                    # and deleted to maintain single source of truth
                    elif client_id not in user_dict.keys():  
                        self.logger.debug(f"disconnection client {str(client_id)} because client was not in FTS core user_dict")
                        self.disconnect_socket(self.clientInformationQueue[client_id][0])
                        del self.clientInformationQueue[client_id]

                    # TODO this case will never happen
                    else:
                        self.logger.error("the data for this client is invalid " + str(client_id))
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as e:
            self.logger.error("exception has been thrown getting client data from queue " + str(e))

    # TODO make raise an exception
    def send_user_connection_geo_chat(self, clientInformation):
        ''' function to create and send pm to newly connected user

        :param clientInformation: the object containing information about the user to which the msg is sent
        :return:
        '''
        # TODO: refactor as it has a proper implementation of a PM to a user generated by the server
        from FreeTAKServer.controllers.SpecificCoTControllers.SendGeoChatController import SendGeoChatController
        from FreeTAKServer.model.RawCoT import RawCoT
        from FreeTAKServer.model.FTSModel.Dest import Dest
        import uuid
        if OrchestratorConstants().DEFAULTCONNECTIONGEOCHATOBJ != None:
            ChatObj = RawCoT()
            ChatObj.xmlString = f'<event><point/><detail><remarks>{OrchestratorConstants().DEFAULTCONNECTIONGEOCHATOBJ}</remarks><marti><dest/></marti></detail></event>'

            classobj = SendGeoChatController(ChatObj, AddToDB=False)
            instobj = classobj.getObject()
            instobj.modelObject.detail._chat.chatgrp.setuid1(clientInformation.modelObject.uid)
            dest = Dest()
            dest.setcallsign(clientInformation.modelObject.detail.contact.callsign)
            instobj.modelObject.detail.marti.setdest(dest)
            instobj.modelObject.detail._chat.setchatroom(clientInformation.modelObject.detail.contact.callsign)
            instobj.modelObject.detail._chat.setparent("RootContactGroup")
            instobj.modelObject.detail._chat.setid(clientInformation.modelObject.uid)
            instobj.modelObject.detail._chat.setgroupOwner("True")
            instobj.modelObject.detail.remarks.setto(clientInformation.modelObject.uid)
            instobj.modelObject.setuid(
                'GeoChat.' + 'SERVER-UID.' + clientInformation.modelObject.detail.contact.callsign + '.' + str(
                    uuid.uuid1()))
            instobj.modelObject.detail._chat.chatgrp.setid(clientInformation.modelObject.uid)
            classobj.reloadXmlString()
            # self.get_client_information()
            self.sent_message_count += 1
            SendDataController().sendDataInQueue(None, instobj, self.clientInformationQueue)
            return 1
        else:
            return 1

    def clientConnected(self, raw_connection_information: RawCoT):
        """ this controls the client connection sequence calling methods which perform the following,
            instantiating the client object, sharing the client with core, adding the client to the db
            and sending the connection message

        :param raw_connection_information:
        :return:
        """
        try:
            from FreeTAKServer.controllers.DatabaseControllers.EventTableController import EventTableController
            clientPipe = None
            self.logger.info(loggingConstants.CLIENTCONNECTED)

            # Instantiate the client object
            clientInformation = self.ClientInformationController.intstantiateClientInformationModelFromConnection(raw_connection_information, clientPipe)

            # TODO remove
            if clientInformation == -1:
                self.logger.info("client had invalid connection information and has been disconnected")
                return -1

            # TODO remove or handle better
            if not self.checkOutput(clientInformation):
                raise Exception('Error in the creation of client information')

            self.openSockets += 1
            # breaks ssl
            try:
                if hasattr(clientInformation.socket, 'getpeercert'):
                    cn = "placeholder"
                else:
                    cn = None
                CoTRow = EventTableController().convert_model_to_row(clientInformation.modelObject)
                self.dbController.create_user(
                    uid=clientInformation.modelObject.uid,
                    callsign=clientInformation.modelObject.detail.contact.callsign,
                    IP=clientInformation.IP, CoT=CoTRow, CN=cn
                )
            except Exception as e:
                self.logger.error(f'There has been an error in a clients connection while adding information to the database {str(e)}')

            self.logger.debug("Adding client...")
            self.add_service_user(client_information=clientInformation)

            # Add client info to queue
            self.clientInformationQueue[clientInformation.modelObject.uid] = [clientInformation.socket]
            self.logger.debug("Client added")

            # Broadcast user in geochat
            self.send_user_connection_geo_chat(clientInformation)
            return clientInformation
        except Exception as e:
            self.logger.warning(loggingConstants.CLIENTCONNECTEDERROR + str(e))
            return -1

    def dataReceived(self, raw_cot: RawCoT):
        """this will be executed in the event that the use case for the CoT isn't specified in the orchestrator

        :param raw_cot: the CoT to be processed and shared
        """
        try:
            # this will check if the CoT is applicable to any specific controllers
            raw_cot = self.XMLCoTController.determineCoTType(raw_cot)

            # the following calls whatever controller was specified by the above function
            module = importlib.import_module('FreeTAKServer.controllers.SpecificCoTControllers.' + raw_cot.CoTType)
            CoTSerializer = getattr(module, raw_cot.CoTType)
            # TODO: improve way in which the dbController is passed to CoTSerializer
            raw_cot.dbController = self.dbController
            processedCoT = CoTSerializer(raw_cot).getObject()

            # this statement checks if the data type is a user update and if so it will be saved to the associated client object
            if raw_cot.CoTType == 'SendUserUpdateController':
                # find entry with this uid
                self.update_client_information(client_information=processedCoT)
            return processedCoT
        except Exception as e:
            self.logger.error(loggingConstants.DATARECEIVEDERROR + str(e))
            return -1

    def clientDisconnected(self, client_information: User):
        """Handles the disconnection of clients

        :param client_information:
        :return:
        """
        import traceback
        self.logger.debug('Disconnecting client')

        # TODO add proper exception handling
        # Get socket info from client object
        try:
            if hasattr(client_information, "clientInformation"):
                client_information = client_information.clientInformation
            sock = self.clientInformationQueue[client_information.user_id][0]
        except Exception as e:
            self.logger.critical("getting sock from client information queue failed " + str(e))
        
        try:
            self.logger.debug('client ' + client_information.m_presence.modelObject.uid + ' disconnected ' + "\n".join(
                traceback.format_stack()))
        except Exception as e:
            self.logger.critical("there was an error logging disconnection information " + str(e))

        # Removes the user id from client info queue
        try:
            del self.clientInformationQueue[client_information.user_id]
        except Exception as e:
            self.logger.critical("client removal failed " + str(e))

        # Remove the active thread and database connection
        try:
            self.ActiveThreadsController.removeClientThread(client_information)
            self.dbController.remove_user(query=f'uid = "{client_information.user_id}"')
        except Exception as e:
            self.logger.critical(f'There has been an error in a clients disconnection while adding information to the database {str(e)}')

        try:
            self.remove_service_user(client_information=client_information)
            self.disconnect_socket(sock)

            self.logger.info(loggingConstants.CLIENTDISCONNECTSTART)

            # TODO: remove string
            tempXml = RawCoT()
            tempXml.xmlString = '<event><detail><link uid="{0}"/></detail></event>'.format(
                client_information.user_id).encode()
            disconnect = SendDisconnectController(tempXml)
            self.get_client_information()
            self.sent_message_count += 1
            self.messages_to_core_count += 1
            SendDataController().sendDataInQueue(disconnect.getObject().clientInformation, disconnect.getObject(),
                                                 self.clientInformationQueue, self.CoTSharePipe)
            self.logger.info(loggingConstants.CLIENTDISCONNECTEND + str(
                client_information.m_presence.modelObject.uid))
            return 1
        except Exception as e:
            import traceback
            import sys, linecache
            exc_type, exc_obj, tb = sys.exc_info()
            f = tb.tb_frame
            lineno = tb.tb_lineno
            filename = f.f_code.co_filename
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            self.logger.error(loggingConstants.CLIENTCONNECTEDERROR + " " + str(e) + " on line: " + line)

    def send_disconnect_cot(self, client_information):
        # TODO: remove string
        tempXml = RawCoT()
        tempXml.xmlString = '<event><detail><link uid="{0}"/></detail></event>'.format(
            client_information.user_id).encode()
        disconnect = SendDisconnectController(tempXml)
        self.get_client_information()
        self.sent_message_count += 1
        self.messages_to_core_count += 1
        SendDataController().sendDataInQueue(
            disconnect.getObject().clientInformation,
            disconnect.getObject(),
            self.clientInformationQueue,
            self.CoTSharePipe
        )

    def disconnect_socket(self, sock: socket.socket) -> None:
        """this method is responsible for disconnecting all socket objects

        :param sock: socket object to be disconnected
        """
        self.logger.debug('Shutting down socket')
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            self.logger.error('Error shutting socket down in client disconnection ' + str(e) + "\n".join(traceback.format_stack()))
        try:
            sock.close()
        except Exception as e:
            self.logger.error(
                'Error closing socket in client disconnection ' + str(e) + "\n".join(traceback.format_stack()))

    def monitor_raw_cot(self, data: RawCoT) -> object:
        """ this method takes as input a sent CoT and calls it's associated function

        this method supports three handlers defined in XMLCoTController which handle, connect, disconnect
        and misc messages respectively

        :param data:
        :return:
        """
        try:
            if isinstance(data, int):
                return None
            else:
                cot = XMLCoTController(logger=self.logger).determineCoTGeneral(data)
                handler = getattr(self, cot[0])
                output = handler(cot[1])
                output.clientInformation = self.clientInformationQueue[data.clientInformation][1]
                return output
        except Exception as e:
            self.logger.error(loggingConstants.MONITORRAWCOTERRORB + str(e))
            return -1

    #TODO Remove or replace
    def checkOutput(self, output):
        """ this method checks whether or not the return data was valid

        :param output: any type which was returned by a function
        :rtype: bool indicating whether the output was valid or not
        """
        if output != -1 and output is not None and isinstance(output, object):
            return True
        else:
            return False

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
        :param receiveConnection:
        :param sock:
        :param pool:
        :param event:
        :param clientDataPipe:
        :param ReceiveConnectionKillSwitch:
        :param CoTSharePipe:
        :param ssl:
        """
        # TODO change to logging
        print('server started')

        # TODO change to self.connection_type
        if ssl:
            print("\n\n running ssl \n\n")
        else:
            threading.Thread(target=self.monitor).start()
        self.ssl = ssl
        import datetime
        import time

        # TODO is this necessary
        receiveconntimeoutcount = datetime.datetime.now()
        lastprint = datetime.datetime.now()
        start_timer = time.time() - 60

        while event.is_set():
            self.CoTSharePipe = CoTSharePipe
            try:
                if ssl == True:
                    pass
                self.clientDataPipe = clientDataPipe
                if event.is_set():
                    try:
                        if ReceiveConnectionKillSwitch.is_set():
                            try:
                                receiveConnection.successful()
                            except:
                                pass
                            ReceiveConnectionKillSwitch.clear()
                            receiveConnection = pool.apply_async(ReceiveConnections().listen,
                                                                 (sock,))
                        else:
                            # print('receiving connection')
                            receiveConnectionOutput = receiveConnection.get(timeout=0.01)
                            self.connection_received += 1
                            print(self.connection_received)
                            receiveConnection = pool.apply_async(ReceiveConnections().listen, (sock, ssl,))
                            receiveconntimeoutcount = datetime.datetime.now()
                            lastprint = datetime.datetime.now()
                            CoTOutput = self.handle_connection_data(receiveConnectionOutput)

                    except multiprocessing.TimeoutError:

                        if (datetime.datetime.now() - receiveconntimeoutcount) > datetime.timedelta(
                                seconds=60) and ssl == True:
                            from multiprocessing.pool import ThreadPool
                            try:
                                pass
                            except Exception as e:
                                print(str(e))
                        elif ssl == True and (datetime.datetime.now() - lastprint) > datetime.timedelta(seconds=30):
                            print('time since last reset ' + str(datetime.datetime.now() - receiveconntimeoutcount))
                            lastprint = datetime.datetime.now()
                        else:
                            pass
                    except Exception as e:
                        self.logger.error('exception in receive connection within main run function ' + str(e))

                    try:
                        clientDataOutput = clientData.get(
                            timeout=0.01)  # attempt to retrieve data from the client reception hndler

                        if self.checkOutput(clientDataOutput) and isinstance(clientDataOutput, list):
                            if clientDataOutput != []:  # just added so log exist of most recent client data output and the time it was sent
                                recent_client_data_output = (clientDataOutput, time.time())
                            self.received_message_count += len(
                                clientDataOutput)  # add the length of this list to the number of received messages
                            CoTOutput = self.handle_regular_data(clientDataOutput)
                        else:
                            clientData = pool.apply_async(ClientReceptionHandler().startup,
                                                          (self.clientInformationQueue,))
                            raise Exception(
                                'client reception handler has returned data which is not of type list data is ' + str(
                                    clientDataOutput))
                        self.get_client_information()
                        clientData = pool.apply_async(ClientReceptionHandler().startup, (self.clientInformationQueue,))
                    except multiprocessing.TimeoutError:
                        pass
                    except Exception as e:
                        self.logger.info('exception in receive client data within main run function ' + str(e))
                        pass
                    try:
                        for x in range(100):
                            if not CoTSharePipe.empty():

                                data = CoTSharePipe.get()
                                self.handle_shared_data(data)
                            else:
                                break
                    except Exception as e:
                        self.logger.error(
                            'there has been an excepion in the handling of data supplied by the rest API ' + str(e))
                        pass
                else:
                    self.stop()
                    break
                try:
                    if time.time() > start_timer + 60:
                        start_timer = time.time()
                        self.logger.debug(str('mainRunFunction is running'))
                        # self.logger.debug('CoTSharePipe is full ' + str(CoTSharePipe.full()))
                        # self.logger.debug('clientDataPipe is full ' + str(clientDataPipe.full()))
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
                pass
        self.stop()

    def handle_shared_data(self, modelData):
        """ this method is responsible for receiving and forwarding data shared via IPC

        :param modelData:
        :return:
        """
        try:
            self.get_client_information()
            self.messages_from_core_count += 1
            if hasattr(modelData, 'clientInformation'):
                self.sent_message_count += 1
                SendDataController().sendDataInQueue(modelData.clientInformation, modelData, self.clientInformationQueue)
            else:
                self.sent_message_count += 1
                SendDataController().sendDataInQueue(None, modelData, self.clientInformationQueue)
        except Exception as e:
            self.logger.error("data base connection error " + str(e))

    def handle_regular_data(self, clientDataOutput: RawCoT):
        """ this method initiates the serializtion and distribution of
        "regular" data being sent by clients. regular data entails data which
        is neither a new connection nor a disconnection.

        :argument clientDataOutput: list of RawCoT objects

        :rtype: None

        """
        try:
            for clientDataOutputSingle in clientDataOutput:
                try:
                    if not self.ssl:
                        self.logger.debug('Handling regular data')
                    if clientDataOutputSingle == -1:
                        continue
                    CoTOutput = self.monitor_raw_cot(clientDataOutputSingle)
                    self.logger.info("cot serialized " + str(CoTOutput.modelObject.uid) )
                    if CoTOutput == 1:
                        continue
                    elif self.checkOutput(CoTOutput):
                        self.get_client_information()
                        self.sent_message_count += 1
                        self.messages_to_core_count += 1
                        output = SendDataController().sendDataInQueue(CoTOutput.clientInformation, CoTOutput,  # pylint: disable=no-member; isinstance checks that CoTOutput is of proper type
                                                                      self.clientInformationQueue, self.CoTSharePipe)
                        if self.checkOutput(output) and isinstance(output, tuple) == False:
                            pass
                        elif isinstance(output, tuple):
                            self.logger.error('issue sending data to client now disconnecting')
                            self.clientDisconnected(output[1])

                        else:
                            self.logger.error('send data failed in main run function with data ' + str(
                                CoTOutput.xmlString) + ' from client ' + CoTOutput.clientInformation.modelObject.detail.contact.callsign)  # pylint: disable=no-member; isinstance checks that CoTOutput is of proper type and should thus have all specified members

                    else:
                        raise Exception('error in general data processing')
                except Exception as e:
                    self.logger.info(
                        'exception in client data, data processing within main run function ' + str(
                            e) + ' data is ' + str(CoTOutput))
        except Exception as e:
            self.logger.info("there has been an error iterating client data output " + str(e))
            return -1
        return 1

    def handle_connection_data(self, receive_connection_output: RawCoT) -> None:
        """this method should be called to initiate the process for receiving new connection data
        :rtype: None
        :param receive_connection_output: a RawCoT object from a newly connected client
        """
        try:
            self.logger.debug('Handling connection data')
            if receive_connection_output == -1:
                return None

            CoTOutput = self.monitor_raw_cot(receive_connection_output)
            if CoTOutput != -1 and CoTOutput != None:
                self.sent_message_count += 1
                output = SendDataController().sendDataInQueue(CoTOutput, CoTOutput, self.clientInformationQueue, self.CoTSharePipe)
                if self.checkOutput(output):
                    self.logger.debug(f'Connection data from client {CoTOutput.modelObject.detail.contact.callsign} successfully processed.')
                else:
                    raise Exception('error in sending data')
        except Exception as e:
            self.logger.error('exception in receive connection data processing within main run function ' + str(
                e) + ' data is ' + str(CoTOutput))
            return -1
        self.sendInternalCoT(CoTOutput)
        return 1

    @abstractmethod
    def start(self, IP, CoTPort, Event, clientDataPipe, ReceiveConnectionKillSwitch, RestAPIPipe, clientDataRecvPipe):
        """this method should be overridden by all inheriting classes and should implement the variables
        type hinted in this abstract class, finally it should be responsible for initiating the mainRunFunction
        """
        self.logger
        self.dbController: DatabaseController
        self.pool: multiprocessing.pool.ThreadPool
        self.clientDataRecvPipe: multiprocessing.Queue

    def stop(self):
        self.clientDataPipe.close()
        self.pool.terminate()
        self.pool.close()
        self.pool.join()

    #TODO move to MonitorConnectionController
    def monitor(self):
        """ this method, which should be run in a thread executes a logging process every 15 seconds.
        The conents of the log entry will contain the following information:
            Messages Sent,
            Messages Received,
            Messages shared with core,
            Messages received from core,
            clients connected currently
        """
        logging_interval = 15

        while True:
            time.sleep(15)
            try:
                self.logger.debug(f"messages sent to clients in {logging_interval} seconds: {self.sent_message_count}")
                self.logger.debug(
                    f"messages received from clients in {logging_interval} seconds: {self.received_message_count}")
                self.logger.debug(
                    f"messages shared with core in {logging_interval} seconds: {self.messages_to_core_count}")
                self.logger.debug(
                    f"messages shared with core in {logging_interval} seconds: {self.messages_from_core_count}")
                self.logger.debug(f"number of connected client: {str(len(self.clientInformationQueue.keys()))}")
                self.sent_message_count = 0
                self.received_message_count = 0
                self.messages_to_core_count = 0
                self.messages_from_core_count = 0
            except Exception as e:
                self.logger.critical("logging service failed with exception " + str(e))
