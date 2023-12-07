"""this file contains the emergency sender controller responsible for transmitting all emergencies"""
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from .emergency_general_controller import EmergencyGeneralController
from ..configuration.emergency_constants import (
    EMERGENCY_ALERT,
    BASE_OBJECT_NAME
)

class EmergencySenderController(Controller):
    """this class is responsible for transmitting emergencies, however it is not used as all routing
    should be going through the main"""

    # internal action mapper is used so that the serialize_emergency controller can be reached
    def __init__(
        self,
        sync_action_mapper: ActionMapper,
        request: Request,
        response: Response,
        configuration: Configuration,
        emergency_action_mapper: ActionMapper,
        
    ):
        super().__init__(request, response, emergency_action_mapper, configuration)
        self.emergency_general_controller = EmergencyGeneralController(request, response, sync_action_mapper, configuration)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def initialize(self, request, response):
        self.request = request
        self.response = response
        self.emergency_general_controller.initialize(request, response)

    def broadcast_emergency(self, model_object, **kwargs):
        """this method will broadcast a specific emergency

        Args:
            emergency_uid (str): the uid of the emergency to be broadcasted
        """
        try:
            self.request.get_value("logger").debug(
                f"broadcasting emergency {model_object.uid}"
            )

            self.response.set_values(kwargs)
            self.request.set_value("model_objects", [model_object])
            self.response.set_action(self.request.get_value("model_object_parser"))

        except Exception as error:
            self.request.get_value("logger").error(
                f"error broadcasting emergency {error}"
            )

    def send_emergencies_to_client(self, config_loader, user, **kwargs):
        """this method will broadcast all emergencies to a specific client"""
        emergencies = self.execute_sub_action("GetAllEmergencies").get_value(
            "emergencies"
        )
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)
        self.emergency_general_controller.initialize(self.request, self.response)
        configuration = config_loader.find_configuration(EMERGENCY_ALERT)
        self.request.set_value("configuration", configuration)
        
        self.response.set_value("message", [])

        # Serializer called by service manager requires the message value
        self.request.set_value("message", [])

        self.response.set_value('recipients', [])

        for emergency in emergencies:
            if self.emergency_general_controller.validate_user_distance(emergency, user):
                self.response.get_value('recipients').append(str(user.get_oid()))
                self.response.get_value("message").append(emergency)
                self.request.get_value("message").append(emergency)

        response = self.execute_sub_action("ValidateUsers")
        
        for emergency in self.response.get_value('message'):
            self.emergency_general_controller.convert_type(emergency)
        
        self.response.set_action('publish')