
from digitalpy.routing.controller import Controller
from ..domain import Event


class DropPointSenderController(Controller):
    """this class is responsible for transmitting points"""

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
            self.execute_sub_action("Broadcast")
        except Exception as error:
            self.request.get_value("logger").error(
                f"error broadcasting point {error}"
            )
