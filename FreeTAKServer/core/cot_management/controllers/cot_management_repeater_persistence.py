import pickle
from typing import Dict, List
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.domain.node import Node
from digitalpy.core.digipy_configuration.configuration import Configuration

from ..configuration.cot_management_constants import PERSISTENCE_PATH

class CotManagementRepeaterPersistence(Controller):
    """this class is responsible for persisting repeated messages
    """
    def __init__(self,
        request: Request,
        response: Response,
        cot_management_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, cot_management_action_mapper, configuration)

    def _save_repeated_messages(self, messages: Dict[str, Node]):
        """save a given message to a json file used for persistency in pickled form

        Args:
            message (Dict[str, Node]): entire messages dictionary to be saved
        """
        with open(PERSISTENCE_PATH, "wb+") as f:
            return pickle.dump(messages, f)
        
    def _load_repeated_messages(self)->Dict[str, Node]:
        """load the pickled saved messages asa dictionary

        Returns:
            Dict[str, Node]: a dictionary of message ids and their associated objects
        """
        try:
            with open(PERSISTENCE_PATH, "rb+") as f:
                try:
                    return pickle.load(f)
                # handle the case where the persistence file is empty in which case we simply return an empty dict and save it to the file
                except EOFError:
                    self._save_repeated_messages({})
                    return {}
        except FileNotFoundError:
            # handle the case where the persistence file doesnt exist in which case we simply return an empty dict and save it to the file
            self._save_repeated_messages({})
            return {}