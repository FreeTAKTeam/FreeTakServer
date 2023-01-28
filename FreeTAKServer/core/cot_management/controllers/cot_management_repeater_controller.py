from digitalpy.core.IAM.model.connection import Connection
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.domain.node import Node

from typing import List, Union

from FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence import CotManagementRepeaterPersistence

class CotManagementRepeaterController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        cot_management_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, cot_management_action_mapper, configuration)
        self.persistency_controller = CotManagementRepeaterPersistence(request, response, cot_management_action_mapper, configuration)

    def initialize(self, request, response):
        self.request = request
        self.response = response

    def connected_user(self, **kwargs):
        """deal with the case of a new connection, this will return all repeated
            messages for which the user is authorized

        Args:
            connection (Connection): the connection object of the new connection (required for `ValidateUsers` and `publish` actions)
        """
        # retrieve all repeated messages
        message = self.persistency_controller._load_repeated_messages()
       
        nodes = []

        # convert the list to a dictionary
        for node in message.values():
            nodes.append(node)

        # set the response value of the messages for the validate users call
        self.response.set_value("message", nodes)

        # validate the users in the recipients list
        response = self.execute_sub_action("ValidateUsers")
        self.response.set_value("message", response.get_value("message"))
        self.response.set_action("publish")

    def get_repeated_messages(self, **kwargs):
        """get all the repeated messages
        """
        # retrieve all repeated messages
        messages = self.persistency_controller._load_repeated_messages()
       
        nodes = []

        # convert the list to a dictionary
        for node in messages.values:
            nodes.append(node)

        # set the response value of the messages
        self.response.set_value("message", nodes)        

    def create_repeated_messages(self, message: List[Node], **kwargs):
        """add a message to be repeated

        Args:
            message (List[Node]): a list of or a single node to be added to repeated messages
        """
        cur_messages = self.persistency_controller._load_repeated_messages()
        if isinstance(message, list):
            for node in message:
                cur_messages[str(node.get_id())] = node
        else:
            cur_messages[str(node.get_id())]
        self.persistency_controller._save_repeated_messages(cur_messages)
        self.response.set_value("success", True)

    def delete_repeated_message(self, ids: List[str], **kwargs):
        """delete a repeated message

        Args:
            ids (Union[List[str], str]): a list of or a single object id of a repeated message to be deleted
        """
        cur_messages = self.persistency_controller._load_repeated_messages()
        for id in ids:
            del cur_messages[id]
        self.persistency_controller._save_repeated_messages(cur_messages)
        self.response.set_value("success", True)