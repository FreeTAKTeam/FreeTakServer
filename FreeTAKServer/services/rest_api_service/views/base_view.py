from flask import request, views
from typing import Dict, List
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response

from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants(log_name="FTS-ManageEmergencyView")
logger = CreateLoggerController("FTS-ManageEmergencyView", logging_constants=loggingConstants).getLogger()

APPLICATION_PROTOCOL = "xml"
# API Request timeout in ms
API_REQUEST_TIMEOUT = 5000

class BaseView(views.View):
    """base class meant to provide the base functionality for
    an FTS API views
    """
    def __init__(self, endpoints: Dict[str, callable]) -> None:
        """the BaseView constructor. Meant to be called by inheriting class'

        Args:
            endpoints (Dict[str, callable]): dictionary containing endpoint names and their associated functions
        """
        self.endpoints = endpoints

    def dispatch_request(self, method: str):
        try:
            return self.endpoints[method]()
        except Exception as ex:
            error_msg = f"error {str(ex)} thrown while executing {method} in {self.__class__.__name__}"
            logger.error(error_msg)
            return error_msg, 500
            

    def make_request(self, action: str, values: Dict = {}, synchronous:bool=True) -> Response:
        """make a request to the zmanager

        Args:
            action (str): the action key to be sent
            values (Dict, optional): the values to be sent in the reques. Defaults to {}.
            synchronous (bool, optional): whether or not to wait for a response from the zmanager. Defaults to True.

        Returns:
            Response: the response coming from the the zmanager
        """
        rest_api_service = ObjectFactory.get_instance("RestAPIService")

        # request to get repeated messages
        request: Request = ObjectFactory.get_new_instance("request")
        request.set_action(action)
        request.set_sender(rest_api_service.__class__.__name__.lower())
        request.set_format("pickled")
        request.set_values(values)
        rest_api_service.subject_send_request(request, APPLICATION_PROTOCOL)
        if synchronous:
            response = rest_api_service.retrieve_response(request.get_id())
            return response