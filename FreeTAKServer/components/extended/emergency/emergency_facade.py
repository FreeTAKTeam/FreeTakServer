from FreeTAKServer.components.core.abstract_component.facade import Facade
from FreeTAKServer.components.extended.emergency.configuration.emergency_constants import (
    CONFIGURATION_PATH_TEMPLATE,
    ACTION_MAPPING_PATH,
    TYPE_MAPPINGS,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
)
from . import domain
from . import controllers
from . import base


# th
class Emergency(Facade):
    """This is the facade class for the emergency component, it is responsible
    for handling all public routing and forwards all requests to the internal routing
    """

    def __init__(
        self,
        emergency_action_mapper,
        request,
        response,
        configuration,
    ):
        super().__init__(
            # the path to the external action mapping
            action_mapping_path=ACTION_MAPPING_PATH,
            # the path to the internal action mapping
            internal_action_mapping_path=INTERNAL_ACTION_MAPPING_PATH,
            # the type mapping in dictionary form
            type_mapping=TYPE_MAPPINGS,
            # the path to the logger configuration
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            # the package containing the base classes
            base=base,
            # the component specific action mapper (passed by constructor)
            action_mapper=emergency_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
        )
