from FreeTAKServer.components.core.abstract_component.facade import Facade
from . import domain
from FreeTAKServer.components.core.cot_router.cot_router_constants import (
    CONFIGURATION_PATH_TEMPLATE,
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
)
from FreeTAKServer.components.core.cot_router.cot_router_main import COTRouter


class COTRouterFacade(Facade):
    def __init__(self, action_mapper, request, response, configuration):
        self.cot_router = COTRouter(
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
        super().__init__(
            config_path_template=CONFIGURATION_PATH_TEMPLATE,
            domain=domain,
            action_mapping_path=ACTION_MAPPING_PATH,
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            controllers=[self.cot_router],
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )

    def cot_received(self, **kwargs):
        self.cot_router.cot_received(**self.request.get_values())

    def cot_broadcast(self, **kwargs):
        self.cot_router.cot_broadcast(**self.request.get_values())
