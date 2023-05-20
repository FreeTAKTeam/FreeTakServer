from FreeTAKServer.services.rest_api_service.views.base_view_controller import BaseViewController
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants

loggingConstants = LoggingConstants(log_name="FTS-ManageConnectionsView")
logger = CreateLoggerController("FTS-ManageConnectionsView", logging_constants=loggingConstants).getLogger()

class ManageConnections(BaseViewController):
    decorators = []
    
    def __init__(self) -> None:
        pass

    def get_users(self):
        response = self.make_request("GetAllConnections", service_id="rest_api_service")
        connections = response.get_value("connections")
        output = []
        for connection in connections:
            try:
                serialized_user = {
                    "callsign": connection.model_object.detail.contact.callsign,
                    "team": connection.model_object.detail._group.name,
                }
                output.append(serialized_user)
            except AttributeError as ex:
                logger.error("emergency model object missing attribute %s", ex)
        return output