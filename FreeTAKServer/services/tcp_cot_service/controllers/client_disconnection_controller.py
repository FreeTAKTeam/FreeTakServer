from typing import Dict
from opentelemetry.trace import Status, StatusCode
from FreeTAKServer.services.tcp_cot_service.controllers.SendDataController import SendDataController
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
import socket
import traceback
from logging import Logger

from FreeTAKServer.core.SpecificCoTControllers.SendDisconnectController import SendDisconnectController
from FreeTAKServer.model.ClientInformation import ClientInformation
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.model.RawCoT import RawCoT
from FreeTAKServer.model.User import User

APPLICATION_PROTOCOL = "XML"
loggingConstants = LoggingConstants()

class ClientDisconnectionController(Controller):
    """ control the process of disconnecting a tcp client
    """
    def __init__(self, logger: Logger, client_information_queue: Dict[str, tuple], active_threads_controller,
                 connections, open_sockets, connection_type):
        self.logger = logger
        self.client_information_queue = client_information_queue
        self.active_threads_controller = active_threads_controller
        self.connections = connections
        self.open_sockets = open_sockets
        self.connection_type = connection_type

    def delete_client_connection(self, clientInformation: str):
        """Handles the disconnection of clients

        Args:
            clientInformation (User): the client information of the client to be disconnected
        """
        # Removes the user id from client info queue
        del self.client_information_queue[clientInformation]
        self.active_threads_controller.removeClientThread(clientInformation)

        try:
            self.logger.info(loggingConstants.CLIENTDISCONNECTSTART)

            # TODO: remove string
            self.logger.info(
                loggingConstants.CLIENTDISCONNECTEND
                + str(clientInformation)
            )
        except Exception as ex:
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
                + str(ex)
                + " on line: "
                + line
            )

    def get_sock(self, client_information) -> socket:
        """get the socket from the client information (this is necessary due to data inconsistency)
        """
        if isinstance(client_information, str):
            return self.client_information_queue[client_information][0]
        elif isinstance(client_information, RawCoT):
            return self.client_information_queue[
                    client_information.clientInformation
                ][0]
        else:
            raise ValueError("invalid client_information parameter type " + str(type(client_information)))

    def remove_client_from_db(self, db_controller, client_information):
        db_controller.remove_user(query=f'uid = "{client_information}"')

    def get_connection_id(self, client_information) -> str:
        """"""
        if hasattr(client_information, "modelObject"):
            uid = client_information.modelObject.uid
        elif hasattr(client_information, "m_presence"):
            uid = client_information.m_presence.modelObject.uid
        elif isinstance(client_information, str):
            uid = client_information
        return str(ObjectFactory.get_instance("ObjectId", {"id": uid, "type": "connection"}))


    def create_iam_disconnect_request(self, connection_id):
        """create a request object which sends a disconnect message to the iam component

        Args:
            clientInformation (_type_): _description_

        Returns:
            _type_: _description_
        """
        request = ObjectFactory.get_new_instance("request")
        request.set_action("disconnection")
        request.set_sender(self.__class__.__name__.lower())
        request.set_value("connection_id", connection_id)
        request.set_format("pickled")
        return request

    def send_disconnect_cot(self, client_information):
        """send the disconnection information for a specific client to all connected clients
        Args:
            clientInformation: client to be displayed as
                disconnected by all connected devices
        """
        # TODO: remove string
        tempXml = RawCoT()
        tempXml.xmlString = '<event><detail><link uid="{0}"/></detail></event>'.format(
            client_information
        ).encode()
        disconnect = SendDisconnectController(tempXml)
        SendDataController().sendDataInQueue(
                    disconnect.getObject().clientInformation,
                    disconnect.getObject(),  # pylint: disable=no-member; isinstance checks that CoTOutput is of proper type
                    self.client_information_queue,
                    None,
                )
        
    def disconnect_socket(self, sock: socket.socket) -> None:
        """this method is responsible for disconnecting all socket objects

        :param sock: socket object to be disconnected
        """
        self.logger.debug("Shutting down socket")
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except Exception as ex:
            # this is a debug log as it will alway throw an error if the client has already closed the socket
            self.logger.debug(
                "Error shutting socket down in client disconnection "
                + str(ex)
                + "\n".join(traceback.format_stack())
            )
        try:
            sock.close()
        except Exception as ex:
            self.logger.error(
                "error closing socket in client disconnection "
                + str(ex)
                + "\n".join(traceback.format_stack())
            )