from FreeTAKServer.components.core.abstract_component.facade import Facade
from FreeTAKServer.components.core.cot_router.base.cot_router_constants import (
    CONFIGURATION_PATH_TEMPLATE,
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
)
from . import controllers
from . import base


class COTRouter(Facade):

    state = None

    def __init__(
        self,
        cotrouter_action_mapper,
        request,
        response,
        configuration,
    ):
        super().__init__(
            config_path_template=CONFIGURATION_PATH_TEMPLATE,
            action_mapping_path=ACTION_MAPPING_PATH,
            internal_action_mapping_path=INTERNAL_ACTION_MAPPING_PATH,
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            controllers=controllers,
            base=base,
            action_mapper=cotrouter_action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
