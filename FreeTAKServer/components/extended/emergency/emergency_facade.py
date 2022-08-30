from FreeTAKServer.components.core.abstract_component.facade import Facade
from FreeTAKServer.components.extended.emergency.base.emergency_constants import (
    CONFIGURATION_PATH_TEMPLATE,
    ACTION_MAPPING_PATH,
    TYPE_MAPPINGS,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
)
from . import domain
from . import controllers
from . import base


class Emergency(Facade):

    state = None

    def __init__(
        self,
        emergency_action_mapper,
        request,
        response,
        configuration,
    ):
        super().__init__(
            config_path_template=CONFIGURATION_PATH_TEMPLATE,
            domain=domain,
            action_mapping_path=ACTION_MAPPING_PATH,
            internal_action_mapping_path=INTERNAL_ACTION_MAPPING_PATH,
            type_mapping=TYPE_MAPPINGS,
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            controllers=controllers,
            base=base,
            action_mapper=emergency_action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
        Emergency.state = self.__dict__
