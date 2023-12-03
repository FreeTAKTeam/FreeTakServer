from asyncio import Queue
import threading
import time
from multiprocessing.pool import ThreadPool
import os
import multiprocessing
from opentelemetry.trace import Status, StatusCode
from typing import List, Dict
from FreeTAKServer.services.tcp_cot_service.controllers.client_disconnection_controller import (
    ClientDisconnectionController,
)
from FreeTAKServer.services.tcp_cot_service.controllers.send_component_data_controller import (
    SendComponentDataController,
)

import traceback

from digitalpy.core.service_management.digitalpy_service import DigitalPyService
from digitalpy.core.domain.node import Node
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.parsing.formatter import Formatter

from FreeTAKServer.model.Enumerations.connectionTypes import ConnectionTypes
from .controllers.TCPSocketController import TCPSocketController
from FreeTAKServer.core.connection.ActiveThreadsController import (
    ActiveThreadsController,
)
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

from FreeTAKServer.core.parsers.XMLCoTController import XMLCoTController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants

from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.model.FTSModel.Event import Event
from FreeTAKServer.model.SpecificCoT.Presence import Presence
from FreeTAKServer.model.User import User
from FreeTAKServer.model.ClientInformation import ClientInformation

from .controllers.client_connection_controller import ClientConnectionController
from .configuration.tcp_cot_service_constants import SERVICE_NAME
from .model.tcp_cot_connection import TCPCoTConnection

from FreeTAKServer.core.configuration.CreateLoggerController import (
    CreateLoggerController,
)

loggingConstants = LoggingConstants()
loggingConstants = LoggingConstants(log_name="TCPCoTService")
logger = CreateLoggerController(
    "TCPCoTService", logging_constants=loggingConstants
).getLogger()

from .controllers.ClientReceptionHandler import ClientReceptionHandler

NODE_TO_XML = "NodeToXML"
GET_MACHINE_READABLE_TYPE = "ConvertHumanReadableToMachineReadable"
APPLICATION_PROTOCOL = "XML"
# MAJOR TODO: Make explicit exception classes!!!


class TCPCoTServiceMain(DigitalPyService):
    """this service is responsible for handling the CoT listener for XML"""

    # TODO: prevent repeat add user
    def __init__(
        self,
        service_id,
        subject_address,
        subject_port,
        subject_protocol,
        integration_manager_address,
        integration_manager_port,
        integration_manager_protocol,
        formatter: Formatter,
    ):
        super().__init__(
            service_id,
            subject_address,
            subject_port,
            subject_protocol,
            integration_manager_address,
            integration_manager_port,
            integration_manager_protocol,
            formatter
        )
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
        self.connections: Dict[
            str, TCPCoTConnection
        ] = {}  # meant to eventually obsolete the client information queue

        # instantiate controllers
        self.ActiveThreadsController = ActiveThreadsController()
        self.ClientInformationController = ClientInformationController()
        self.ReceiveConnections = ReceiveConnections()
        self.ReceiveConnectionsProcessController = ReceiveConnectionsProcessController()
        self.XMLCoTController = XMLCoTController()
        self.dbController: DatabaseController
        self.send_component_data_controller = SendComponentDataController(self.logger)
        self.client_connection_controller = ClientConnectionController(
            self.logger,
            self.client_information_queue,
            self.connections,
            self.openSockets
        )
        self.client_disconnection_controller = ClientDisconnectionController(
            self.logger,
            self.client_information_queue,
            self.ActiveThreadsController,
            self.connections,
            self.openSockets,
            self.connection_type,
        )

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
            self.tracer: Tracer = tracing_provider_instance.create_tracer(SERVICE_NAME)

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
            raise ex

    @property
    def connection_type(self):
        return ConnectionTypes.TCP

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
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as ex:
            with self.tracer.start_as_current_span("update_client_information") as span:
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
                        self.client_information_queue[client_id][1] = user_dict[
                            client_id
                        ]
            else:
                self.logger.critical("client data pipe is Full !")
        except Exception as ex:
            with self.tracer.start_as_current_span("get_client_information") as span:
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(ex)

    def component_handler(self, xml_cot):
        """this method is responsible for handling cases where the cot sent should
        be handled (parsed and manipulated) by a specific component it is
        responsible for calling the routing (via the async action mapper)
        of the CoT data

        Args:
            xml_cot (str): xml representation of CoT
        """

        dict_cot = self.convert_xml_to_dict(xml_cot)

        request = ObjectFactory.get_new_instance("request")
        # must get a new instance of the async action mapper for each request
        # to prevent run conditions and to prevent responses going to the wrong
        # callers
        response = ObjectFactory.get_new_instance("response")

        # instantiate and define the request
        request = ObjectFactory.get_new_instance("request")
        request.set_format("pickled")
        human_readable_type = self.get_human_readable_type(dict_cot)
        request.set_action(human_readable_type)
        dict_cot["event"]["@type"] = human_readable_type
        request.set_context("XMLCoT")
        request.set_sender(self.__class__.__name__.lower())
        request.set_value("dictionary", dict_cot)

        # instantiate and define the response
        response = ObjectFactory.get_new_instance("response")
        response.set_format("pickled")

        # final request for the actual cot but listener is not returned because
        # it should be handled by the main loop which listens for all responses
        # with a request source of Orchestrator
        self.logger.debug("sending request to subject %s", str(request.get_values()))
        self.subject_send_request(request, APPLICATION_PROTOCOL)

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
                if isinstance(response.get_value("message"), list):
                    for model_object in response.get_value("message"):
                        self.send_component_message(response, model_object)
                else:
                    self.send_component_message(response, response.get_value("message"))
            except Exception as ex:
                self.logger.error(
                    f"There was an exception sending a single response:\n"
                    f"Sender: {sender}\n"
                    f"Context: {response.get_context()}\n"
                    f"Action: {response.get_action()}\n"
                    f"Exception: {str(ex)}"
                )
                self.logger.debug(
                    "single response exception traceback: %s", traceback.format_exc()
                )

    def send_component_message(self, request, message):
        self.send_component_data_controller.send_message(
            self.connections, message, request.get_value("recipients")
        )

    def send_message(self, sender, message, use_share_pipe=True):
        return SendDataController().sendDataInQueue(
            sender,
            message,  # pylint: disable=no-member; isinstance checks that CoTOutput is of proper type
            self.client_information_queue,
            self.CoTSharePipe,
        )

    def convert_xml_to_dict(self, data) -> dict:
        """convert the xml format to a dict containing the same data via the xml_serializer
        component.

        Args:
            data (str): an xml string containing the data from a given client

        Returns:
            dict: dictionary representation of the cot data
        """
        request = ObjectFactory.get_new_instance("request")
        request.set_action("XMLToDict")
        request.set_value("message", data)

        actionmapper = ObjectFactory.get_instance("syncactionMapper")
        response = ObjectFactory.get_new_instance("response")
        actionmapper.process_action(request, response)

        # dictionary representation of the xml
        data_dict = response.get_value("dict")
        return data_dict

    def get_human_readable_type(self, dict_cot: dict) -> str:
        """parse the cot type and send request to the type component to
        convert it to a human readable type

        Args:
            dict_cot (dict): cot message in dictionary format

        Returns:
            str: the human readable
        """
        # this convert the machine readable type to a human readable type
        request = ObjectFactory.get_new_instance("request")
        request.set_format("pickled")
        request.set_action("ConvertMachineReadableToHumanReadable")
        request.set_context("MEMORY")
        request.set_value("machine_readable_type", dict_cot["event"]["@type"])
        request.set_value("default", dict_cot["event"]["@type"])

        # must get a new instance of the async action mapper for each request
        # to prevent run conditions and to prevent responses going to the wrong
        # callers
        actionmapper = ObjectFactory.get_instance("syncactionMapper")
        response = ObjectFactory.get_new_instance("response")
        actionmapper.process_action(request, response)
        return response.get_value("human_readable_type")

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
                                (sock,),
                            )
                            receiveconntimeoutcount = datetime.datetime.now()
                            lastprint = datetime.datetime.now()
                            CoTOutput = self.handle_connection(
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
                            self.handle_regular_data(clientDataOutput)
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
                                "most recent client data %s",
                                str(recent_client_data_output),
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
                self.send_message(
                    modelData.clientInformation, modelData, use_share_pipe=False
                )
            else:
                self.sent_message_count += 1
                self.send_message(None, modelData, use_share_pipe=False)
        except Exception as ex:
            self.logger.error("data base connection error " + str(ex))

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
            for data_object in clientDataOutput:
                try:
                    logger.debug(f"begginning processing {data_object.xmlString}")
                    # Skip this iteration if the data is invalid
                    if data_object == -1:
                        continue
                    elif data_object.xmlString == b"":
                        self.handle_disconnection(data_object.clientInformation)
                        continue
                    # Process the raw CoT data and serialize it
                    self.component_handler(data_object.xmlString)
                    self.logger.debug(f"finished processing {data_object.xmlString}")

                except Exception as ex:
                    self.logger.error(
                        f"Exception in client data processing within main run function {ex} data is {data_object.xmlString} trace is {traceback.format_exc()}"
                    )
                    continue
        except Exception as ex:
            self.logger.info(f"Error iterating client data output {ex}")
            return -1
        return 1

    def handle_disconnection(self, client_information):
        """handle a client disconnection from the service by disconnecting the socket and informing clients of the disconnection

        Args:
            client_information (_type_): _description_
        """
        sock = self.client_disconnection_controller.get_sock(client_information)
        
        self.client_disconnection_controller.delete_client_connection(client_information)

        self.client_disconnection_controller.disconnect_socket(sock)

        connection_id = self.client_disconnection_controller.get_connection_id(client_information)

        iam_disconnect_request = self.client_disconnection_controller.create_iam_disconnect_request(connection_id)
        self.subject_send_request(iam_disconnect_request, APPLICATION_PROTOCOL)

        self.client_disconnection_controller.send_disconnect_cot(client_information)

    def handle_connection(self, receive_connection_output: RawCoT) -> None:
        """this method should be called to initiate the process for receiving new connection data
        :rtype: None
        :param receive_connection_output: a RawCoT object from a newly connected client
        """
        try:
            self.logger.debug("Handling connection data")
            if receive_connection_output == -1:
                return None

            client_connection, client_information = self.client_connection_controller.create_client_connection(
                receive_connection_output, self.dbController
            )
            self.client_connection_controller.save_client_to_db(client_information, self.dbController)
            
            iam_request = self.client_connection_controller.create_iam_request(client_connection)
            self.subject_send_request(iam_request, APPLICATION_PROTOCOL)
            
            repeated_messages_request = self.client_connection_controller.create_send_repeated_messages_request(client_connection)
            self.subject_send_request(repeated_messages_request, APPLICATION_PROTOCOL)
            
            send_emergencies_request = self.client_connection_controller.create_send_emergencies_request(client_connection)
            self.subject_send_request(send_emergencies_request, APPLICATION_PROTOCOL)

            self.client_connection_controller.send_user_connection_geo_chat(client_information)

            # self.handle_regular_data([receive_connection_output])

        except Exception as e:
            self.logger.error(
                "exception in receive connection data processing within main run function "
                + str(e)
            )
            self.logger.debug(
                "with traceback: %s", traceback.format_exc()
            )
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
                    f"number of connected client: {str(len(self.connections.keys()))}"
                )
                self.sent_message_count = 0
                self.received_message_count = 0
                self.messages_to_core_count = 0
                self.messages_from_core_count = 0
            except Exception as e:
                self.logger.critical("logging service failed with exception " + str(e))
