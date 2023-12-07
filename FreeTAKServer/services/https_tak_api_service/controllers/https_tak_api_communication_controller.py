from digitalpy.core.service_management.controllers.service_management_communication_controller import ServiceManagementCommunicationController
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.services.https_tak_api_service.https_tak_api_service_main import APPLICATION_PROTOCOL

class HTTPSTakApiCommunicationController(ServiceManagementCommunicationController):
    def __init__(self):
        super().__init__("https_tak_api_service", "HTTPSTakAPIService", "xml", None, None, None, None)
