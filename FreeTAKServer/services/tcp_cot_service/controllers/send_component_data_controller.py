from typing import Dict

from FreeTAKServer.services.tcp_cot_service.model.tcp_cot_connection import TCPCoTConnection
from ..configuration.tcp_cot_service_constants import MessageTypes

from digitalpy.core.main.controller import Controller

import logging

class SendComponentDataController(Controller):
    def __init__(self, logger) -> None:
        self.logger = logger

    def send_message(self, connections, message, recipients, **kwargs):
        message_type = self.determine_message_type(recipients)
        if message_type == MessageTypes.SEND_TO_ALL:
            self.send_message_to_all(connections, message)
        
        elif message_type == MessageTypes.SEND_TO_SOME:
            self.send_message_to_some(connections, message, recipients)

    def determine_message_type(self, recipients) -> MessageTypes:
        """determine whether the message is to be sent to all or only
        some connections based on the value of recipients

        Returns:
            MessageTypes: _description_
        """
        if recipients is None or recipients == []:
            return MessageTypes.SEND_TO_ALL
        else:
            return MessageTypes.SEND_TO_SOME
    
    def send_message_to_some(self, connections:Dict[str, TCPCoTConnection], message: bytes, recipients):
        """send a given message to some connections based on value of recipients

        Args:
            connections (dict[str, TCPCoTConnection]): a dictionary of connections indexed by their OIDs
            message (bytes): the message to be sent to some clients
        """
        
        for oid in recipients:
            connection = connections.get(oid)
            if connection != None:
                self.logger.debug("sending: %s, to: %s", str(message), str(connection))
                try:
                    connection.sock.send(message)
                except TimeoutError:
                    self.logger.debug("failed to send message to %s with timeout error", str(connection.get_oid()))
                except BrokenPipeError:
                    self.logger.warning("failed to send message to %s with broken pipe error", str(connection.get_oid()))
                except OSError as os_err:
                    self.logger.warning("failed to send message to %s with os error %s", str(connection.get_oid()), str(os_err))

    def send_message_to_all(self, connections:Dict[str, TCPCoTConnection], message: bytes):
        """send a message to all connections

        Args:
            connections (dict[str, TCPCoTConnection]): a dictionary of connections indexed by their OIDs
            message (bytes): the message to be sent to some clients
        """
        self.logger.debug("sending %s to %s", message, connections)
        for connection in connections.values():
            try:
                connection.sock.send(message)
            except TimeoutError:
                self.logger.debug("failed to send message to %s with timeout error", str(connection.get_oid()))
            except BrokenPipeError:
                self.logger.warning("failed to send message to %s with broken pipe error", str(connection.get_oid()))
            except OSError as os_err:
                self.logger.warning("failed to send message to %s with os error %s", str(connection.get_oid()), str(os_err))