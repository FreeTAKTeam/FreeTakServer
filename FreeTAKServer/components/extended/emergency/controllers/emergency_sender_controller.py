"""this file contains the emergency sender controller responsible for transmitting all emergencies"""
from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.routing.action_mapper import ActionMapper
from digitalpy.config.configuration import Configuration


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
    ):
        super().__init__(request, response, emergency_action_mapper, configuration)

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

    def send_emergencies_to_client(self, **kwargs):
        """this method will broadcast all emergencies to a specific client"""
        emergencies = self.execute_sub_action("GetAllEmergencies").get_value(
            "emergencies"
        )
        model_objects = list(emergencies)
        messages = []
        for emergency in list(emergencies):
            # for each emergency we need to serialize it to the desired format
            self.request.set_value("model_object", emergency)
            sub_response = self.execute_sub_action("SerializeEmergency")
            messages.append(sub_response.get_value("serialized_message"))
        self.response.set_value("model_object", model_objects)
        self.response.set_value("serialized_message", messages)
