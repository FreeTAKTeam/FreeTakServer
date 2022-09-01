from FreeTAKServer.components.core.abstract_component.facade import Facade
from .configuration.type_constants import (
    ACTION_MAPPING_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
)
from . import base


class Type(Facade):

    state = None

    def __init__(self, type_action_mapper, request, response, configuration):

        super().__init__(
            config_path_template=None,
            action_mapping_path=ACTION_MAPPING_PATH,
            internal_action_mapping_path=INTERNAL_ACTION_MAPPING_PATH,
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            domain=None,
            action_mapper=type_action_mapper,
            base=base,
            request=request,
            response=response,
            configuration=configuration,
        )
