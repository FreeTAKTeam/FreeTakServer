from flask import request, views
from typing import Dict, List
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.main.controller import Controller

from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController

loggingConstants = LoggingConstants(log_name="FTS-ManageEmergencyView")
logger = CreateLoggerController("FTS-ManageEmergencyView", logging_constants=loggingConstants).getLogger()

APPLICATION_PROTOCOL = "xml"
# API Request timeout in ms
API_REQUEST_TIMEOUT = 5000

class BaseView(Controller):
    """base class meant to provide the base functionality for
    an FTS API views
    """

    def set_endpoints(self, endpoints: dict):
        """set a new endpoint mapping, this should be called by an API controller at instantiation

        Args:
            endpoints (dict): a mapping of endpoint names to the handling methods
        """
        self.endpoints = endpoints
    
    def get_endpoints(self)->dict:
        """return the endpoints mapped

        Returns:
            dict: the mapped endpoints
        """
        return self.endpoints

    def dispatch_request(self, method: str):
        try:
            return self.endpoints[method]()
        except Exception as ex:
            error_msg = f"error {str(ex)} thrown while executing {method} in {self.__class__.__name__}"
            logger.error(error_msg)
            return error_msg, 500
            

    def make_request(self, action: str, values: Dict = {}, synchronous:bool=True, service_id:str=None) -> Response:
        """make a request to the zmanager

        Args:
            action (str): the action key to be sent
            values (Dict, optional): the values to be sent in the reques. Defaults to {}.
            synchronous (bool, optional): whether or not to wait for a response from the zmanager. Defaults to True.
            service_id (str, optional): what service to share the request response with. Defaults to None.
        Returns:
            Response: the response coming from the the zmanager
        Raises:
            ValueError: raised when synchronous is true and service_id is neither None or rest api service id as this
                            will result in an undefined state where we are waiting for a response that will never come
        """
        rest_api_service = ObjectFactory.get_instance("RestAPIService")
        service_id_different = service_id is not None and rest_api_service.service_id != service_id
        if synchronous == True and service_id_different:
            raise ValueError("synchronous is true and service_id is neither None or rest api service id,\
                              this will result in an undefined state where we are waiting for a response that will never come")

        # request to get repeated messages
        request: Request = ObjectFactory.get_new_instance("request")
        request.set_action(action)
        request.set_sender(rest_api_service.__class__.__name__.lower())
        request.set_format("pickled")
        request.set_values(values)
        rest_api_service.subject_send_request(request, APPLICATION_PROTOCOL, service_id)
        if synchronous == True:
            response = rest_api_service.retrieve_response(request.get_id())
            return response