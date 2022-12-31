from asyncio import Queue
import threading
import time
import traceback
from multiprocessing.pool import ThreadPool
import os
import multiprocessing
import importlib
import socket
from opentelemetry.trace import Status, StatusCode
from typing import List, Union

from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.domain.node import Node
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.parsing.formatter import Formatter

from FreeTAKServer.model.Enumerations.connectionTypes import ConnectionTypes
from .controllers.TCPSocketController import TCPSocketController
from FreeTAKServer.core.util.geo_manager_controller import GeoManagerController
from FreeTAKServer.core.connection.ActiveThreadsController import ActiveThreadsController
from FreeTAKServer.core.connection.ClientInformationController import (
    ClientInformationController,
)
from FreeTAKServer.core.persistence.DatabaseController import (
    DatabaseController,
)
from .controllers.ReceiveConnections import ReceiveConnections
from FreeTAKServer.core.connection.ReceiveConnectionsProcessController import (
    ReceiveConnectionsProcessController,
)

from .controllers.SendDataController import SendDataController
from FreeTAKServer.core.SpecificCoTControllers.SendDisconnectController import (
    SendDisconnectController,
)
from FreeTAKServer.core.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants

from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.core.configuration.OrchestratorConstants import (
    OrchestratorConstants,
)
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.SpecificCoT.Presence import Presence
from FreeTAKServer.model.TCPConnection import TCPConnection
from FreeTAKServer.model.User import User
from FreeTAKServer.model.ClientInformation import ClientInformation

from .configuration.tcp_cot_service_constants import SERVICE_NAME
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
loggingConstants = LoggingConstants()
loggingConstants = LoggingConstants(log_name="FTS-TCP_CoT_Service")
logger = CreateLoggerController(
    "FTS-TCP_CoT_Service", logging_constants=loggingConstants
).getLogger()

from .controllers.ClientReceptionHandler import ClientReceptionHandler

NODE_TO_XML = "NodeToXML"
GET_MACHINE_READABLE_TYPE = "ConvertHumanReadableToMachineReadable"
APPLICATION_PROTOCOL = "COT"
# MAJOR TODO: Make explicit exception classes!!!


class TCPCoTServiceMain(DigitalPyService):
    """this service is responsible for handling the CoT listener for XML"""

    # TODO: prevent repeat add user
    def __init__(self, service_id: str, subject_address: str, subject_port: int, subject_protocol, integration_manager_address: str, integration_manager_port: int, integration_manager_protocol: str, formatter: Formatter):
        super().__init__(service_id, subject_address, subject_port, subject_protocol, integration_manager_address, integration_manager_port, integration_manager_protocol, formatter)
        self.logger = logger

        # Server info
        self.connection_received = 0
        self.sent_message_count = 0
        self.received_message_count = 0
        self.messages_to_core_count = 0
        self.messages_from_core_count = 0
        self.openSockets = 0

        # Contains info on clients
        self.client_information_queue = {}
        self.clientDataPipe: Queue

        # instantiate controllers
        self.ActiveThreadsController = ActiveThreadsController()
        self.ClientInformationController = ClientInformationController()
        self.ReceiveConnections = ReceiveConnections()
        self.ReceiveConnectionsProcessController = ReceiveConnectionsProcessController()
        self.XMLCoTController = XMLCoTController()
        self.dbController: DatabaseController

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
        tracing_provider_instance
    ):
        try:
            # configure the object factory with the passed factory instance
            ObjectFactory.configure(factory)

            # instantiate the tracer instance for this service
            self.tracer: Tracer = tracing_provider_instance.create_tracer(
                SERVICE_NAME
            )
            
            actionmapper = ObjectFactory.get_instance("actionMapper")
            # subscribe to responses originating from this controller
            actionmapper.add_topic(
                f"/routing/response/{self.__class__.__name__.lower()}"
            )

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
                ClientReceptionHandler().startup, (self.client_information_queue,)
            )
            self.initialize_connections(APPLICATION_PROTOCOL)
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
        except Exception as ex:
            return ex
        
    @property
    def connection_type(self):
        return ConnectionTypes.TCP    

    def remove_service_user(self, clientInformation: ClientInformation):
        """Generates the presence object from the
        clientInformation parameter and sends it as a remove message
        to the client data pipe

        Args:
            clientInformation: Client information

        Returns: None
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():

                # Process removal of client in clientDataPipe
                # TODO add blocking
                self.clientDataPipe.put(
                    [
                        "remove",
                        clientInformation,
                        self.openSockets,
                        self.connection_type,
                    ]
                )
                self.logger.debug(
                    f"Client removal has been sent through queue {str(clientInformation)}"
                )
            else:
                self.logger.critical("Client data pipe is full!")
        except Exception as ex:
            with self.tracer.start_as_current_span("remove_service_user") as span:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(ex)
            raise ex

    def update_client_information(self, clientInformation: ClientInformation):
        """Generates a Presence object from the clientInformation parameter and
        sends it as an update message to the client data pipe.

        :param clientInformation: Client information

        Returns: None
        """
        try:
            # TODO this doesnt guarantee that put call will succeed, need to implement blocking...
            if not self.clientDataPipe.full():
                presence_object = Presence()
                presence_object.setModelObject(clientInformation.modelObject)
                presence_object.setXmlString(clientInformation.xmlString.decode())
                presence_object.setClientInformation(clientInformation.modelObject)

                # TODO add blocking
                self.clientDataPipe.put(
                    ["update", presence_object, self.openSockets, None]
                )
                self.logger.debug(
                    "client update has been sent through queue "
                    + str(clientInformation)
                )
                # Add client info to queue
                self.client_information_queue[clientInformation.modelObject.uid][
                    1
                ] = clientInformation
                self.get_client_information()
                # update the geo manager controller with the new client information
                GeoManagerController.update_users(self.client_information_queue)
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as ex:
            with self.tracer.start_as_current_span("update_client_information") as span:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(ex)
            raise ex

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
        except Exception as ex:
            with self.tracer.start_as_current_span("add_service_user") as span:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(ex)
            raise ex

    def get_client_information(self):
        """this method gets client information from the client information pipe and returns it as a dict merged
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
                client_information_queue_client_ids = copy.copy(
                    list(self.client_information_queue.keys())
                )

                for client_id in client_information_queue_client_ids:
                    # forces FTS core to be single source of truth
                    if (
                        client_id in user_dict.keys()
                        and len(self.client_information_queue[client_id]) == 1
                    ):
                        self.client_information_queue[client_id].append(
                            user_dict[client_id]
                        )

                    elif (
                        client_id in user_dict.keys()
                        and len(self.client_information_queue[client_id]) == 2
                    ):
                        self.client_information_queue[client_id][1] = user_dict[client_id]

                    # if the entry isn't present in FTS core than the client will be disconnected
                    # and deleted to maintain single source of truth
                    elif client_id not in user_dict.keys():
                        self.logger.debug(
                            f"disconnection client {str(client_id)} because client was not in FTS core user_dict"
                        )
                        self.disconnect_socket(
                            self.client_information_queue[client_id][0]
                        )
                        del self.client_information_queue[client_id]

                    # TODO this case will never happen
                    else:
                        self.logger.error(
                            "the data for this client is invalid " + str(client_id)
                        )
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as ex:
            with self.tracer.start_as_current_span("get_client_information") as span:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(ex)

    # TODO make raise an exception
    def send_user_connection_geo_chat(self, clientInformation):
        """function to create and send pm to newly connected user

        :param clientInformation: the object containing information about the user to which the msg is sent
        :return:
        """
        # TODO: refactor as it has a proper implementation of a PM to a user generated by the server
        from FreeTAKServer.core.SpecificCoTControllers.SendGeoChatController import (
            SendGeoChatController,
        )
        from FreeTAKServer.model.RawCoT import RawCoT
        from FreeTAKServer.model.FTSModel.Dest import Dest
        import uuid

        if OrchestratorConstants().DEFAULTCONNECTIONGEOCHATOBJ != None:
            ChatObj = RawCoT()
            ChatObj.xmlString = f"<event><point/><detail><remarks>{OrchestratorConstants().DEFAULTCONNECTIONGEOCHATOBJ}</remarks><marti><dest/></marti></detail></event>"

            classobj = SendGeoChatController(ChatObj, AddToDB=False)
            instobj = classobj.getObject()
            instobj.modelObject.detail._chat.chatgrp.setuid1(
                clientInformation.modelObject.uid
            )
            dest = Dest()
            dest.setcallsign(clientInformation.modelObject.detail.contact.callsign)
            instobj.modelObject.detail.marti.setdest(dest)
            instobj.modelObject.detail._chat.setchatroom(
                clientInformation.modelObject.detail.contact.callsign
            )
            instobj.modelObject.detail._chat.setparent("RootContactGroup")
            instobj.modelObject.detail._chat.setid(clientInformation.modelObject.uid)
            instobj.modelObject.detail._chat.setgroupOwner("True")
            instobj.modelObject.detail.remarks.setto(clientInformation.modelObject.uid)
            instobj.modelObject.setuid(
                "GeoChat."
                + "SERVER-UID."
                + clientInformation.modelObject.detail.contact.callsign
                + "."
                + str(uuid.uuid1())
            )
            instobj.modelObject.detail._chat.chatgrp.setid(
                clientInformation.modelObject.uid
            )
            classobj.reloadXmlString()
            # self.get_client_information()
            self.sent_message_count += 1
            self.send_message(None, instobj, use_share_pipe=False)
            return 1
        else:
            return 1

    def clientConnected(self, raw_connection_information: RawCoT):
        """Controls the client connection sequence, calling methods which perform the following:
            1. Instantiate the client object
            2. Share the client with core
            3. Add the client to the database
            4. Send the connection message

        :param raw_connection_information: RawCoT object containing client connection information
        :return: ClientInformation object for the newly connected client, or -1 if there was an error
        """
        try:
            from FreeTAKServer.core.persistence.EventTableController import EventTableController

            self.logger.info(loggingConstants.CLIENTCONNECTED)

            # Instantiate the client object
            clientInformation = self.ClientInformationController.intstantiateClientInformationModelFromConnection(
                raw_connection_information, None
            )
            if clientInformation == -1:
                self.logger.info("Client had invalid connection information and has been disconnected")
                return -1

            # Add client to database
            try:
                if hasattr(clientInformation.socket, "getpeercert"):
                    cn = "placeholder"
                else:
                    cn = None
                CoT_row = EventTableController().convert_model_to_row(clientInformation.modelObject)
                self.dbController.create_user(
                    uid=clientInformation.modelObject.uid,
                    callsign=clientInformation.modelObject.detail.contact.callsign,
                    IP=clientInformation.IP,
                    CoT=CoT_row,
                    CN=cn,
                )
            except Exception as ex:
                with self.tracer.start_as_current_span("clientConnected") as span:
                    span.set_status(Status(StatusCode.ERROR))
                    span.record_exception(ex)

            self.logger.debug("Adding client...")
            self.add_service_user(clientInformation=clientInformation)

            # Add client info to queue
            self.client_information_queue[clientInformation.modelObject.uid] = [clientInformation.socket, clientInformation]
            # Update the geo manager controller with the new client information
            GeoManagerController.update_users(self.client_information_queue)
            self.logger.debug("Client added")

            # Broadcast user in geochat
            self.send_user_connection_geo_chat(clientInformation)

            # Send emergency information to newly connected client
            request = ObjectFactory.get_new_instance("request")
            request.set_action("SendEmergenciesToClient")
            request.set_sender(self.__class__.__name__.lower())
            request.set_value("client_uid", clientInformation.modelObject.uid)
            request.set_value("model_object_parser", "ParseModelObjectToXML")
            request.set_format("pickled")
            actionmapper = ObjectFactory.get_instance("actionMapper")
            response = ObjectFactory.get_new_instance("response")
            actionmapper.process_action(request, response, False)

            return clientInformation
        except Exception as e:
            self.logger.warning(loggingConstants.CLIENTCONNECTEDERROR)


    def dataReceived(self, raw_cot: RawCoT):
        """this will be executed in the event that the use case for the CoT isn't specified in the orchestrator

        :param raw_cot: the CoT to be processed and shared
        """
        try:
            # this will check if the CoT is applicable to any specific controllers
            raw_cot = self.XMLCoTController.determineCoTType(raw_cot)

            # the following calls whatever controller was specified by the above function
            module = importlib.import_module(
                "FreeTAKServer.core.SpecificCoTControllers." + raw_cot.CoTType
            )
            CoTSerializer = getattr(module, raw_cot.CoTType)
            # TODO: improve way in which the dbController is passed to CoTSerializer
            raw_cot.dbController = self.dbController
            processedCoT = CoTSerializer(raw_cot).getObject()

            # this statement checks if the data type is a user update and if so it will be saved to the associated client object
            if raw_cot.CoTType == "SendUserUpdateController":
                # find entry with this uid
                self.update_client_information(clientInformation=processedCoT)
            return processedCoT
        except Exception as e:
            self.logger.error(loggingConstants.DATARECEIVEDERROR + str(e))
            return -1

    def clientDisconnected(self, clientInformation: User):
        """Handles the disconnection of clients

        :param clientInformation:
        :return:
        """
        import traceback

        self.logger.debug("Disconnecting client")

        # TODO add proper exception handling
        # Get socket info from client object
        try:
            if isinstance(clientInformation, str):
                clientInformation = self.client_information_queue[clientInformation][1]
            elif isinstance(clientInformation, RawCoT):
                clientInformation = self.client_information_queue[
                    clientInformation.clientInformation
                ][1]
            sock = self.client_information_queue[clientInformation.user_id][0]
        except Exception as e:
            self.logger.critical(
                "getting sock from client information queue failed " + str(e)
            )

        try:
            self.logger.debug(
                "client "
                + clientInformation.m_presence.modelObject.uid
                + " disconnected "
                + "\n".join(traceback.format_stack())
            )
        except Exception as e:
            self.logger.critical(
                "there was an error logging disconnection information " + str(e)
            )

        # Removes the user id from client info queue
        try:
            del self.client_information_queue[clientInformation.user_id]
            # update the geo manager controller with the new client information
            GeoManagerController.update_users(self.client_information_queue)
        except Exception as e:
            self.logger.critical("client removal failed " + str(e))

        # Remove the active thread and database connection
        try:
            self.ActiveThreadsController.removeClientThread(clientInformation)
            self.dbController.remove_user(query=f'uid = "{clientInformation.user_id}"')
        except Exception as e:
            self.logger.critical(
                f"There has been an error in a clients disconnection while adding information to the database {str(e)}"
            )

        try:
            self.remove_service_user(clientInformation=clientInformation)
            self.disconnect_socket(sock)

            self.logger.info(loggingConstants.CLIENTDISCONNECTSTART)

            # TODO: remove string
            self.send_disconnect_cot(clientInformation)
            self.logger.info(
                loggingConstants.CLIENTDISCONNECTEND
                + str(clientInformation.m_presence.modelObject.uid)
            )
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
            self.logger.error(
                loggingConstants.CLIENTCONNECTEDERROR
                + " "
                + str(e)
                + " on line: "
                + line
            )

    def send_disconnect_cot(self, clientInformation):
        """send the disconnection information for a specific client to all connected clients
        Args:
            clientInformation: client to be displayed as
                disconnected by all connected devices
        """
        # TODO: remove string
        tempXml = RawCoT()
        tempXml.xmlString = '<event><detail><link uid="{0}"/></detail></event>'.format(
            clientInformation.user_id
        ).encode()
        disconnect = SendDisconnectController(tempXml)
        self.get_client_information()
        self.sent_message_count += 1
        self.messages_to_core_count += 1
        self.send_message(disconnect.getObject().clientInformation, disconnect.getObject())

    def disconnect_socket(self, sock: socket.socket) -> None:
        """this method is responsible for disconnecting all socket objects

        :param sock: socket object to be disconnected
        """
        self.logger.debug("Shutting down socket")
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            self.logger.error(
                "Error shutting socket down in client disconnection "
                + str(e)
                + "\n".join(traceback.format_stack())
            )
        try:
            sock.close()
        except Exception as e:
            self.logger.error(
                "error closing socket in client disconnection "
                + str(e)
                + "\n".join(traceback.format_stack())
            )

    def component_handler(self, cot):
        """this method is responsible for handling cases where the cot sent should
        be handled (parsed and manipulated) by a specific component it is
        responsible for calling the routing (via the async action mapper)
        of the CoT data"""
        if not hasattr(cot, "xmlString"):
            raise ValueError("cot missing required attribute 'xmlString'")

        request = ObjectFactory.get_new_instance("request")
        # must get a new instance of the async action mapper for each request
        # to prevent run conditions and to prevent responses going to the wrong
        # callers
        actionmapper = ObjectFactory.get_instance("actionMapper")
        response = ObjectFactory.get_new_instance("response")

        # instantiate and define the request
        request = ObjectFactory.get_new_instance("request")
        request.set_format("pickled")
        request.set_action(cot.data_dict["event"]["@type"])
        request.set_context("XML")
        request.set_sender(self.__class__.__name__.lower())
        request.set_value("dictionary", cot.data_dict)

        # instantiate and define the response
        response = ObjectFactory.get_new_instance("response")
        response.set_format("pickled")

        # final request for the actual cot but listener is not returned because
        # it should be handled by the main loop which listens for all responses
        # with a request source of Orchestrator
        self.subject_send_request(request, APPLICATION_PROTOCOL)
        
        # one is returned so that the message is ignored and can be processed later once the
        # response is received by the component receiver
        return 1

    def convert_to_xml(self, model_object: Node) -> str:
        """call the domain component to convert the model object to xml
        Args:
            model_object (Node): the model object to convert it's xml representation

        Returns:
            str: xml string representation of the model object
        """
        # TODO: this should probably be moved out to a separate controller but
        # in the mean time while we refactor the code base this is an acceptable
        # solution to keep things logically seperated
        # get a sync action mapper
        sync_action_mapper = ObjectFactory.get_instance("syncactionmapper")

        # get the machine readable type of the model object
        request = ObjectFactory.get_instance("request")
        response = ObjectFactory.get_instance("response")

        request.set_action(GET_MACHINE_READABLE_TYPE)
        request.set_value("human_readable_type", model_object.type)

        sync_action_mapper.process_action(request, response)

        model_object.type = response.get_value("machine_readable_type")

        # convert the model object to xml
        request = ObjectFactory.get_instance("request")
        response = ObjectFactory.get_instance("response")

        request.set_action(NODE_TO_XML)
        request.set_value("node", model_object)

        sync_action_mapper.process_action(request, response)

        return response.get_value("message")

    def component_receiver(self):
        """this method is responsible for waiting for the response, enabling
        the response to be sent by the main process responsible for sending
        CoT's. This handler simply returns an empty list in the case that there is no
        data to receive however if data is available from the /routing/response/
        topic it will be received parsed and returned so that it might be sent to
        all clients by the main loop
        """
        responses = self.broker_receive()
        return responses

    def broadcast_component_responses(self) -> None:
        """
        Broadcast responses from the routing proxy to connected ATAK clients.

        This method retrieves the responses from the component_receiver and converts
        them into a format that can be accepted by the SendDataController. It then
        sends the converted responses to the appropriate ATAK clients using the
        send_message method.
        """

        # TODO: This is bad practice but I didn't want to include this import
        # at the beginning of the file so it's going to be here until we work
        # out a way to negate the requirement of the SpecificCoT class or
        # we can include it's instantiation during the component processing.
        from FreeTAKServer.model.SpecificCoT.SendOther import SendOther

        # Get the responses from the routing proxy
        responses = self.component_receiver()

        for response in responses:
            try:
                # Get the sender of the initial cot data
                sender = response.get_sender()

                # Check if the response model object is a list
                if isinstance(response.get_value("model_object"), list):
                    for model_object in response.get_value("model_object"):
                        # Define the specific cot object
                        cot_object = SendOther()
                        cot_object.modelObject = model_object

                        # TODO: Decide where the serialization should be performed.
                        # For now it's performed within the actions called by the routing worker
                        # to reduce the CPU consumption in the current process.
                        cot_object.xmlString = response.get_value("serialized_message").pop()

                        self.send_message(sender, cot_object)
                else:
                    # Get the model object from the response
                    model_object = response.get_value("model_object")

                    # Define the specific cot object
                    cot_object = SendOther()
                    cot_object.modelObject = model_object

                    # TODO: Decide where the serialization should be performed.
                    # For now it's performed by whatever process is receiving the data
                    # in this case using the convert_to_xml method.
                    cot_object.xmlString = self.convert_to_xml(model_object)

                    self.send_message(sender, cot_object)
            except Exception as e:
                self.logger.error(
                    f"There was an exception sending a single response:\n"
                    f"Sender: {sender}\n"
                    f"Model object: {model_object}\n"
                    f"Source: {response.get_source()}\n"
                    f"Context: {response.get_context()}\n"
                    f"Action: {response.get_action()}\n"
                )

    def send_message(self, sender, message, use_share_pipe=True):
        return SendDataController().sendDataInQueue(
                    sender,
                    message,  # pylint: disable=no-member; isinstance checks that CoTOutput is of proper type
                    self.client_information_queue,
                    self.CoTSharePipe,
                )

    def monitor_raw_cot(self, data: RawCoT) -> object:
        """
        This method takes as input a sent CoT and calls its associated function. This method supports three handlers defined
        in XMLCoTController which handle connect, disconnect, and misc messages respectively.

        Args:
            data (RawCoT): The raw CoT data to be processed.

        Returns:
            object: The output of the handler function called on the CoT data.
        """
        try:
            if isinstance(data, int):
                return None
            else:
                cot = XMLCoTController(logger=self.logger).determineCoTGeneral(data, self.client_information_queue)
                handler_name, handler_data = cot
                handler = getattr(self, handler_name, None)
                if handler is None:
                    self.logger.error(f"No handler found for {handler_name}")
                    return -1
                output = handler(handler_data)
                if output != 1:  # when the process is a disconnect the output is 1
                    output.clientInformation = self.client_information_queue[data.clientInformation][1]
                return output
        except Exception as e:
            self.logger.error(loggingConstants.MONITORRAWCOTERRORB + str(e))
            return -1

    # TODO Remove or replace
    def checkOutput(self, output):
        """this method checks whether or not the return data was valid

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
        ssl=False,
    ):
        """This is the central method which is responsable for the functioning of the CoT service's it iterates over
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
        print("server started")

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
                            receiveConnection = pool.apply_async(
                                ReceiveConnections().listen, (sock,)
                            )
                        else:
                            # print('receiving connection')
                            receiveConnectionOutput = receiveConnection.get(
                                timeout=0.01
                            )
                            self.connection_received += 1
                            print(self.connection_received)
                            receiveConnection = pool.apply_async(
                                ReceiveConnections().listen,
                                (
                                    sock,
                                ),
                            )
                            receiveconntimeoutcount = datetime.datetime.now()
                            lastprint = datetime.datetime.now()
                            CoTOutput = self.handle_connection_data(
                                receiveConnectionOutput
                            )

                    except multiprocessing.TimeoutError:

                        if (
                            datetime.datetime.now() - receiveconntimeoutcount
                        ) > datetime.timedelta(seconds=60) and ssl == True:
                            from multiprocessing.pool import ThreadPool

                            try:
                                pass
                            except Exception as e:
                                print(str(e))
                        elif ssl == True and (
                            datetime.datetime.now() - lastprint
                        ) > datetime.timedelta(seconds=30):
                            print(
                                "time since last reset "
                                + str(datetime.datetime.now() - receiveconntimeoutcount)
                            )
                            lastprint = datetime.datetime.now()
                        else:
                            pass
                    except Exception as e:
                        self.logger.error(
                            "exception in receive connection within main run function "
                            + str(e)
                        )

                    try:
                        clientDataOutput = clientData.get(
                            timeout=0.01
                        )  # attempt to retrieve data from the client reception hndler

                        if self.checkOutput(clientDataOutput) and isinstance(
                            clientDataOutput, list
                        ):
                            if (
                                clientDataOutput != []
                            ):  # just added so log exist of most recent client data output and the time it was sent
                                recent_client_data_output = (
                                    clientDataOutput,
                                    time.time(),
                                )
                            self.received_message_count += len(
                                clientDataOutput
                            )  # add the length of this list to the number of received messages
                            CoTOutput = self.handle_regular_data(clientDataOutput)
                        else:
                            clientData = pool.apply_async(
                                ClientReceptionHandler().startup,
                                (self.client_information_queue,),
                            )
                            raise Exception(
                                "client reception handler has returned data which is not of type list data is "
                                + str(clientDataOutput)
                            )
                        self.get_client_information()
                        clientData = pool.apply_async(
                            ClientReceptionHandler().startup,
                            (self.client_information_queue,),
                        )
                    except multiprocessing.TimeoutError:
                        pass
                    except Exception as e:
                        self.logger.info(
                            "exception in receive client data within main run function "
                            + str(e)
                        )
                        pass
                    try:
                        # 100 is an arbitrary number of cots to receive from other
                        # services to prevent the process from getting stuck receiving data from
                        # other services
                        for x in range(100):
                            if not CoTSharePipe.empty():

                                data = CoTSharePipe.get()
                                self.handle_shared_data(data)
                            else:
                                break
                    except Exception as e:
                        self.logger.error(
                            "there has been an excepion in the handling of data supplied by the rest API "
                            + str(e)
                        )
                        pass

                    try:
                        self.broadcast_component_responses()
                    except Exception as e:
                        self.logger.error(
                            "exception broadcasting component responses " + str(e)
                        )

                else:
                    self.stop()
                    break
                try:
                    if time.time() > start_timer + 60:
                        start_timer = time.time()
                        self.logger.debug(str("mainRunFunction is running"))
                        # self.logger.debug('CoTSharePipe is full ' + str(CoTSharePipe.full()))
                        # self.logger.debug('clientDataPipe is full ' + str(clientDataPipe.full()))
                        if "recent_client_data_output" in locals():
                            self.logger.debug(
                                "most recent client data "
                                + str(recent_client_data_output)
                            )
                            self.logger.debug(
                                "time since last valid data "
                                + str(time.time() - recent_client_data_output[1])
                            )
                            self.logger.debug(
                                "content of last valid data "
                                + str(recent_client_data_output[0][0].xmlString)
                            )
                        self.logger.debug(
                            "client dict: " + str(self.client_information_queue)
                        )
                except Exception as e:
                    self.logger.error(
                        "the periodic debug message has thrown an error " + str(e)
                    )
            except Exception as e:
                self.logger.info(
                    "there has been an uncaught error thrown in mainRunFunction"
                    + str(e)
                )
                pass
        self.stop()

    def handle_shared_data(self, modelData):
        """this method is responsible for receiving and forwarding data shared via IPC

        :param modelData:
        :return:
        """
        try:
            self.get_client_information()
            self.messages_from_core_count += 1
            if hasattr(modelData, "clientInformation"):
                self.sent_message_count += 1
                self.send_message(modelData.clientInformation, modelData, use_share_pipe=False)
            else:
                self.sent_message_count += 1
                self.send_message(None, modelData, use_share_pipe=False)
        except Exception as e:
            self.logger.error("data base connection error " + str(e))

    def handle_sub_message(self, message):
        with self.tracer.start_as_current_span("handle_sub_message") as span:
            if message[0] == "/outbound/cots":
                span.add_event("outbound cot received")
                if hasattr(message[1], "clientInformation"):
                    self.sent_message_count += 1
                    self.send_message(message[1].clientInformation, message[1], use_share_pipe=False)
                else:
                    self.sent_message_count += 1
                    self.send_message(None, message[1], use_share_pipe=False)
    
    def handle_regular_data(self, clientDataOutput: List[RawCoT]):
        """
        Handle "regular" data being sent by clients. Regular data is data that is neither a new connection nor a disconnection.

        This method initiates the serialization and distribution of regular data.

        Args:
            clientDataOutput (List[RawCoT]): List of RawCoT objects

        Returns:
            None
        """
        # Iterate through each piece of client data
        try:
            for clientDataOutputSingle in clientDataOutput:
                try:
                    # Skip this iteration if the data is invalid
                    if clientDataOutputSingle == -1:
                        continue

                    # Process the raw CoT data and serialize it
                    CoTOutput = self.monitor_raw_cot(clientDataOutputSingle)
                    self.logger.info(f"CoT serialized {CoTOutput.modelObject.uid}")

                    # Skip this iteration if the CoT data is invalid
                    if CoTOutput == 1:
                        continue

                    # Check if the CoT data is valid and can be sent
                    if self.checkOutput(CoTOutput):
                        # Get client information and send the message
                        self.get_client_information()
                        self.sent_message_count += 1
                        self.messages_to_core_count += 1
                        output = self.send_message(CoTOutput.clientInformation, CoTOutput)

                        # Check if the message was sent successfully
                        if self.checkOutput(output) and not isinstance(output, tuple):
                            # Message was sent successfully
                            pass
                        elif isinstance(output, tuple):
                            # There was an issue sending the message, so disconnect the client
                            self.logger.error("Issue sending data to client, now disconnecting")
                            self.clientDisconnected(output[1])
                        else:
                            # There was an issue sending the message
                            self.logger.error(f"Send data failed with data {CoTOutput.xmlString} from client {CoTOutput.clientInformation.modelObject.detail.contact.callsign}")
                    else:
                        # The CoT data is invalid, raise an exception
                        raise Exception("Error in general data processing")
                except Exception as e:
                    self.logger.info(f"Exception in client data processing within main run function {e} data is {CoTOutput}")
        except Exception as e:
            self.logger.info(f"Error iterating client data output {e}")
            return -1
        return 1


    def handle_connection_data(self, receive_connection_output: RawCoT) -> None:
        """this method should be called to initiate the process for receiving new connection data
        :rtype: None
        :param receive_connection_output: a RawCoT object from a newly connected client
        """
        try:
            self.logger.debug("Handling connection data")
            if receive_connection_output == -1:
                return None

            CoTOutput = self.monitor_raw_cot(receive_connection_output)
            if CoTOutput != -1 and CoTOutput != None and CoTOutput != 1:
                self.sent_message_count += 1
                output = self.send_message(CoTOutput, CoTOutput)

                if self.checkOutput(output):
                    self.logger.debug(
                        f"Connection data from client {CoTOutput.modelObject.detail.contact.callsign} successfully processed."
                    )
                else:
                    raise Exception("error in sending data")
        except Exception as e:
            self.logger.error(
                "exception in receive connection data processing within main run function "
                + str(e)
                + " data is "
                + str(CoTOutput)
            )
            return -1
        return 1

    def stop(self):
        self.clientDataPipe.close()
        self.pool.terminate()
        self.pool.close()
        self.pool.join()

    # TODO move to MonitorConnectionController
    def monitor(self):
        """this method, which should be run in a thread executes a logging process every 15 seconds.
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
                self.logger.debug(
                    f"messages sent to clients in {logging_interval} seconds: {self.sent_message_count}"
                )
                self.logger.debug(
                    f"messages received from clients in {logging_interval} seconds: {self.received_message_count}"
                )
                self.logger.debug(
                    f"messages shared with core in {logging_interval} seconds: {self.messages_to_core_count}"
                )
                self.logger.debug(
                    f"messages shared with core in {logging_interval} seconds: {self.messages_from_core_count}"
                )
                self.logger.debug(
                    f"number of connected client: {str(len(self.client_information_queue.keys()))}"
                )
                self.sent_message_count = 0
                self.received_message_count = 0
                self.messages_to_core_count = 0
                self.messages_from_core_count = 0
            except Exception as e:
                self.logger.critical("logging service failed with exception " + str(e))
