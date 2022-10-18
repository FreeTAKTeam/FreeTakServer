
from digitalpy.routing.controller import Controller
from ..domain import Event
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.routing.action_mapper import ActionMapper
from digitalpy.config.configuration import Configuration


class DropPointSenderController(Controller):
    """this class is responsible for transmitting points"""

    def __init__(
        self,
        request: Request,
        response: Response,
        drop_point_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, drop_point_action_mapper, configuration)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def broadcast_drop_point(self, model_object: Event, **kwargs):
        """this method will broadcast a drop point
        """
        try:
            self.request.get_value("logger").debug(
                f"broadcasting point {model_object.uid}"
            )

            self.response.set_values(kwargs)
            self.request.set_value("model_objects", [model_object])
            self.execute_sub_action(self.request.get_value("model_object_parser"))
        except Exception as error:
            self.request.get_value("logger").error(
                f"error broadcasting drop point {error}"
            )
