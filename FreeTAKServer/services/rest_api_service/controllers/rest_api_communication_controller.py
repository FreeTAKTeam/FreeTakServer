from digitalpy.core.service_management.controllers.service_management_communication_controller import ServiceManagementCommunicationController

class RestAPICommunicationController(ServiceManagementCommunicationController):
    def __init__(self):
        super().__init__("rest_api_service", "RestAPIService", "json", None, None, None, None)