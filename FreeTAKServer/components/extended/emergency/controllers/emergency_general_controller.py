from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.routing.action_mapper import ActionMapper
from digitalpy.config.configuration import Configuration


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

        # serialize the emergency model object in a sub-action
        response = self.execute_sub_action(
            self.request.get_value("model_object_parser")
        )
        # add the serialized model object to the controller response as a value
        self.response.set_value(
            "serialized_message", response.get_value("serialized_message")
        )
