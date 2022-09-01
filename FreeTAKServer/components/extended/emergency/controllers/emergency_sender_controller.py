from digitalpy.routing.controller import Controller
from ..domain import Event


class EmergencySenderController(Controller):
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def broadcast_emergency(self, model_object: Event, **kwargs):
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
            self.execute_sub_action("Broadcast")
        except Exception as error:
            self.request.get_value("logger").error(
                f"error broadcasting emergency {error}"
            )

    def broadcast_all_emergencies(self, **kwargs):
        """this method will broadcast all emergencies
        Args:
        """
        self.response.set_values(kwargs)
        self.response.set_action("Broadcast")
        emergencies = self.execute_sub_action("EmergencyGetAll").get_value(
            "emergencies"
        )
        self.response.set_value("model_objects", list(emergencies))
