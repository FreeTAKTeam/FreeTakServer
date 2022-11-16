from digitalpy.component.impl.default_facade import DefaultFacade
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from FreeTAKServer.components.core.domain.configuration.domain_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
)
from . import base


class Domain(DefaultFacade):
    """This is the facade class for the domain component, it is responsible
    for handling all public routing and forwards all requests to the internal routing
    """

    def __init__(
        self,
        domain_action_mapper,
        request,
        response,
        configuration,
        tracing_provider_instance=None,
    ):
        super().__init__(
            # the path to the external action mapping
            action_mapping_path=ACTION_MAPPING_PATH,
            # the path to the internal action mapping
            internal_action_mapping_path=INTERNAL_ACTION_MAPPING_PATH,
            # the path to the logger configuration
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            # the package containing the base classes
            base=base,
            # the component specific action mapper (passed by constructor)
            action_mapper=domain_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # log file path
            log_file_path=MainConfig.LogFilePath,
            # the tracing provider used
            tracing_provider_instance=tracing_provider_instance,
        )
