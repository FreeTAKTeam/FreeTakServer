from digitalpy.core.IAM.model.connection import Connection
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.domain.node import Node

from typing import List, Union

from FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence import CotManagementRepeaterPersistence
from FreeTAKServer.core.cot_management.controllers.cot_management_geo_object_controller import CotManagementGeoObjectController
# used for type hinting
from FreeTAKServer.components.core.domain.domain import Event

class CotManagementRepeaterController(Controller):
    """this class is responsible for handling the business logic regarding the repeated messages
    """
    def __init__(
        self,
        request: Request,
        response: Response,
        cot_management_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, cot_management_action_mapper, configuration)
        self.persistency_controller = CotManagementRepeaterPersistence(request, response, cot_management_action_mapper, configuration)
        self.geo_object_cotroller = CotManagementGeoObjectController(request, response, cot_management_action_mapper, configuration)

    def initialize(self, request, response):
        self.geo_object_cotroller.initialize(request, response)
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
            print(message)

        # set the response value of the messages for the validate users call
        self.response.set_value("message", nodes)

        # validate the users in the recipients list
        # TODO figure out better way of accessing external actions (actions in other components)
        #response = self.execute_sub_action("ValidateUsers")
        #self.response.set_value("recipients", response.get_value("recipients"))
        self.response.set_action("publish")

        # copy request values to response
        for key, value in self.request.get_values().items():
            self.response.set_value(key, value)
            #  print(response)

    def get_repeated_messages(self, **kwargs):
        """get all the repeated messages
        """
        # retrieve all repeated messages
        messages = self.persistency_controller._load_repeated_messages()
       
        nodes = []

        # convert the list to a dictionary
        for node in messages.values():
            nodes.append(node)

        # set the response value of the messages
        self.response.set_value("message", nodes)

        # copy request values to response
        for key, value in self.request.get_values().items():
            self.response.set_value(key, value)
            
    def create_repeated_messages(self, message: List[Event], **kwargs):
        """add a message to be repeated

        Args:
            message (List[Event]): a list of events to be added to repeated messages.
        """
        # load existing repeated messages
        cur_messages = self.persistency_controller._load_repeated_messages()
        # iterate the passed list of nodes and add each one to the dict of current messages with the oid as the
        # key and the object as the value
        for node in message:
            # use the event id 
            cur_messages[str(node.uid)] = node
        # save the updated dict of current messages
        self.persistency_controller._save_repeated_messages(cur_messages)
        # return that the operation was successful
        self.response.set_value("success", True)

    def delete_repeated_message(self, ids: List[str], **kwargs):
        """delete a repeated message

        Args:
            ids (List[str]): a list of object ids of repeated messages to be deleted
        """
        # load existing repeated messages
        cur_messages = self.persistency_controller._load_repeated_messages()
        
        # iterate through passed ids and remove each one from the current repeated messages
        for id in ids:
            if id in cur_messages:
                del cur_messages[id]

        # save the repeated messages with passed id's deleted
        self.persistency_controller._save_repeated_messages(cur_messages)

        # return that the operation was successful
        self.response.set_value("success", True)