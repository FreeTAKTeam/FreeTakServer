from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory
from FreeTAKServer.components.core.COT_router.configuration.COT_router_constants import (
    BASE_OBJECT_NAME,
    BASE_COT,
)


class COTRouter(Controller):
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())

    def cot_broadcast(self, model_object, **kwargs):
        self.request.get_value("logger").debug("broadcast CoT")
        self.response.set_values(kwargs)
        self.request.set_value("model_objects", [model_object])

        self.execute_sub_action("Broadcast")

    def cot_received(self, logger, **kwargs):
        self.response.set_values(kwargs)

        logger.debug("received cot message")

        self.request.set_value("message_type", BASE_COT)
        self.request.set_value("object_class_name", BASE_OBJECT_NAME)

        response = self.execute_sub_action("CreateNode")

        self.request.set_value("model_object", response.get_value("model_object"))

        self.request.set_value("message", self.request.get_value("message").xmlString)

        response = self.execute_sub_action("ParseCoT")

        self.response.set_value("model_object", response.get_value("model_object"))
        self.execute_sub_action("CoTBroadcast")
