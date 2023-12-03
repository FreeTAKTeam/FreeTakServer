from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.domain.node import Node
from typing import List

class CoTManagementPrivateCoTController(Controller):
    """this class contains the business logic responsible for extracting the reipients from
    cots with a distinct target"""

    def __init__(
        self,
        request: Request,
        response: Response,
        action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, action_mapper, configuration)

    def get_recipients(self, model_object: Node)->List[str]:
        """this method is responsible for getting the recipients of a given cot message
        based on it's model object representation

        Args:
            model_object (Node): the model_object of the CoT from which the recipients should be extracted

        Returns:
            List[str]: a list containing the callsigns of all recipients for the cot or an empty list if the message
            is to be sent to all clients
        """
        recipients = []
        if model_object == None:
            print("empty object")
        # validate the Marti tag exists
        if not hasattr(model_object.detail, "marti") or len(model_object.detail.marti.dest)<1 or model_object.detail.marti.dest[0].callsign == None:
            return "*"

        sub_response = self.execute_sub_action("GetAllConnections")
        for dest in model_object.detail.marti.dest:
            for con in sub_response.get_value("connections"):
                if dest.callsign == con.model_object.detail.contact.callsign:
                    recipients.append(str(con.get_oid()))

        return recipients
