from digitalpy.core.service_management.controllers.service_management_communication_controller import ServiceManagementCommunicationController
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration


class HTTPTakApiCommunicationController(ServiceManagementCommunicationController):
    def __init__(self):
        super().__init__("http_tak_api_service", "HTTPTakAPIService", "xml", None, None, None, None)
