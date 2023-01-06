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
        request: Request,
        response: Response,
        emergency_action_mapper: ActionMapper,
        configuration: Configuration,
        sync_action_mapper: ActionMapper,
    ):
        super().__init__(request, response, emergency_action_mapper, configuration)
        self.emergency_general_controller = EmergencyGeneralController(request, response, sync_action_mapper, configuration)
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

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
        model_objects = list(emergencies)
        configuration = config_loader.find_configuration(EMERGENCY_ALERT)
        self.request.set_value("configuration", configuration)
        for emergency in model_objects:
            self.emergency_general_controller.add_user_to_marti(emergency, user)
        self.response.set_value("model_object", model_objects)
