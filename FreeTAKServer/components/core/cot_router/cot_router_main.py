from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory
from FreeTAKServer.components.core.cot_router.cot_router_constants import (
    BASE_OBJECT_NAME,
    BASE_COT,
)


class COTRouter(Controller):
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())

    def cot_broadcast(self, model_object, **kwargs):
        self.request.get_value("logger").debug("broadcast CoT")
        self.response.set_values(kwargs)
        self.response.set_action("Broadcast")
        self.response.set_value("model_objects", [model_object])

    def cot_received(self, message, logger, **kwargs):
        self.response.set_values(kwargs)

        logger.debug("received cot message")

        facade = ObjectFactory.get_instance(self.request.get_sender())

        empty_model_object = facade.create_node(BASE_COT, BASE_OBJECT_NAME)

        self.request.set_value("message", message.xmlString)
        self.request.set_value("model_object", empty_model_object)

        response = self.execute_sub_action("ParseCoT")

        self.response.set_value("model_object", response.get_value("model_object"))
        self.response.set_action("CoTBroadcast")
