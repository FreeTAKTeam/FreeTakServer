from FreeTAKServer.core.configuration.OrchestratorConstants import OrchestratorConstants
from FreeTAKServer.services.tcp_cot_service.controllers.SendDataController import SendDataController
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.main.controller import Controller

from opentelemetry.trace import Status, StatusCode

from logging import Logger

from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.persistence.EventTableController import EventTableController
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.core.connection.ClientInformationController import (
    ClientInformationController,
)
from FreeTAKServer.model.TCPConnection import TCPConnection
from FreeTAKServer.model.SpecificCoT.Presence import Presence

from ..model.tcp_cot_connection import TCPCoTConnection

APPLICATION_PROTOCOL = "XML"
loggingConstants = LoggingConstants()

class ClientConnectionController(Controller):
    """manage the connection of new clients
    """

    def __init__(self, logger: Logger, client_information_queue, connections, open_sockets):
        self.client_information_controller = ClientInformationController()
        self.logger = logger
        self.client_information_queue = client_information_queue
        self.connections = connections
        self.open_sockets = open_sockets

    def create_client_connection(self, raw_connection_information: RawCoT, db_controller) -> TCPConnection:
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
            clientInformation = self.client_information_controller.intstantiateClientInformationModelFromConnection(
                raw_connection_information, None
            )
            if clientInformation == -1:
                self.logger.info("Client had invalid connection information and has been disconnected")
                return -1

            # Add client to database
            self.save_client_to_db(clientInformation, db_controller)

            # Add client info to queue
            self.client_information_queue[clientInformation.modelObject.uid] = [clientInformation.socket, clientInformation]
            
            # instantiate an object_id with a value of the client uid
            object_id = ObjectFactory.get_new_instance("ObjectId", dynamic_configuration={"id": clientInformation.modelObject.uid, "type": "connection"})
            
            # TODO the instantiation of the connection object and the connection action
            # call should be moved out of the tcp_cot_service main and into the connection
            # controller

            # instantiate a new TCPCoTConnection with an object_id of the client uid
            connection = TCPCoTConnection(object_id)
            connection.model_object = clientInformation.modelObject
            connection.sock = clientInformation.socket
            self.connections[str(connection.get_oid())] = connection

            return connection, clientInformation
        except Exception as ex:
            self.logger.warning(loggingConstants.CLIENTCONNECTEDERROR + str(ex))

    def save_client_to_db(self, clientInformation, db_controller):
        try:
            if hasattr(clientInformation.socket, "getpeercert"):
                cn = "placeholder"
            else:
                cn = None
            CoT_row = EventTableController().convert_model_to_row(clientInformation.modelObject)
            db_controller.create_user(
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

    def create_iam_request(self, connection: TCPConnection):
        """register the client with the IAM component

        Args:
            connection (TCPConnection): connection object of new client
        """
        request = ObjectFactory.get_new_instance("request")
        request.set_action("connection")
        request.set_sender(self.__class__.__name__.lower())
        request.set_value("connection", connection)
        request.set_format("pickled")
        return request

    def create_send_repeated_messages_request(self, connection: TCPConnection):
        """send the repeated messages to the new client with the repeated messages components

        Args:
            connection (TCPConnection): connection object of new client
        """
        request = ObjectFactory.get_new_instance("request")
        request.set_sender(self.__class__.__name__.lower())
        request.set_action("connection")
        request.set_context("Repeater")
        request.set_value("connection", connection)
        request.set_value("recipients", [str(connection.get_oid())])
        request.set_format("pickled")
        return request
        

    def create_send_emergencies_request(self, connection: TCPConnection):
        """send the active emergencies to the new client with the emergencies component

        Args:
            connection (TCPConnection): connection object of new client
        """
        request = ObjectFactory.get_new_instance("request")
        request.set_action("SendEmergenciesToClient")
        request.set_sender(self.__class__.__name__.lower())
        request.set_value("user", connection)
        request.set_format("pickled")
        return request

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
            SendDataController().sendDataInQueue(
                    None,
                    instobj,  # pylint: disable=no-member; isinstance checks that CoTOutput is of proper type
                    self.client_information_queue,
                    None,
                )