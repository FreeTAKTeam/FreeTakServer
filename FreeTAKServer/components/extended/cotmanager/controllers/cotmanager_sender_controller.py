"""this file contains the component sender controller responsible for transmitting all components"""
from digitalpy.routing.controller import Controller
from cotmanager.domain import Event
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.routing.action_mapper import ActionMapper
from digitalpy.config.configuration import Configuration


class COTManagerSenderController(Controller):
    """this class is responsible for transmitting components, however it is not used as all routing
    should be going through the main"""

    # internal action mapper is used so that the serialize_component  controller can be reached
    def __init__(
        self,
        request: Request,
        response: Response,
        cotmanager_action_mapper: ActionMapper,
        configuration: Configuration,
    ):
        super().__init__(request, response, cotmanager_action_mapper, configuration)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def broadcast_cotmanager(self, model_object: Event, **kwargs):
        """this method will broadcast the component
        """
        try:
            self.request.get_value("logger").debug(
                "broadcasting component"
            )

            self.response.set_values(kwargs)
            self.request.set_value("model_objects", [model_object])
            self.response.set_action(self.request.get_value("model_object_parser"))

        except Exception as error:
            self.request.get_value("logger").error(
                f"error broadcasting component {error}"
            )

