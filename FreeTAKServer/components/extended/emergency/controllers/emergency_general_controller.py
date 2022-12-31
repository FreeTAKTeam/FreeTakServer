from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration


class EmergencyGeneralController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ):
        super().__init__(request, response, sync_action_mapper, configuration)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def serialize_emergency(self, **kwargs):
        """this is the general method used to serialize the emergency to a given format"""
        # serialize the emergency model object in a sub-action
        response = self.execute_sub_action(
            self.request.get_value("model_object_parser")
        )
        # add the serialized model object to the controller response as a value
        self.response.set_value(
            "serialized_message", response.get_value("serialized_message")
        )
        self.request.get_value("logger").debug(
            "serialized emergency message to format "
            + self.request.get_value("model_object_parser")
        )
