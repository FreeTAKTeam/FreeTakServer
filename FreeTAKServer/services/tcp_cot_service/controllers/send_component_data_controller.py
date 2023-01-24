from FreeTAKServer.services.tcp_cot_service.model.tcp_cot_connection import TCPCoTConnection
from ..configuration.tcp_cot_service_constants import MessageTypes

from digitalpy.core.main.controller import Controller

class SendComponentDataController(Controller):
    def __init__(self, request, response, action_mapper, configuration) -> None:
        super().__init__(request, response, action_mapper, configuration)

    def send_message(self, connections, message, recipients, **kwargs):
        message_type = self.determine_message_type(recipients)
        if message_type == MessageTypes.SEND_TO_ALL:
            self.send_message_to_all(connections, message)
        
        elif message_type == MessageTypes.SEND_TO_SOME:
            self.send_message_to_some(connections, message)

    def determine_message_type(self, recipients) -> MessageTypes:
        """determine whether the message is to be sent to all or only
        some connections based on the value of recipients

        Returns:
            MessageTypes: _description_
        """
        if recipients == None or recipients == []:
            return MessageTypes.SEND_TO_ALL
        else:
            return MessageTypes.SEND_TO_SOME
    
    def send_message_to_some(self, connections: dict[str, TCPCoTConnection], message: bytes):
        """send a given message to some connections based on value of recipients

        Args:
            connections (dict[str, TCPCoTConnection]): a dictionary of connections indexed by their OIDs
            message (bytes): the message to be sent to some clients
        """
        recipient_oids = self.request.get_value("recipients")
        
        for oid in recipient_oids:
            connection = connections.get(oid)
            if oid != None:
                connection.sock.send(message)

    def send_message_to_all(self, connections: dict[str, TCPCoTConnection], message: bytes):
        """send a message to all connections

        Args:
            connections (dict[str, TCPCoTConnection]): a dictionary of connections indexed by their OIDs
            message (bytes): the message to be sent to some clients
        """
        for connection in connections.values():
            connection.sock.send(message)