from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from .configuration.type_constants import (
    ACTION_MAPPING_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    MANIFEST_PATH,
)
from . import base

config = MainConfig.instance()


class Type(DefaultFacade):

    state = None

    def __init__(
        self,
        type_action_mapper,
        request,
        response,
        configuration,
        tracing_provider_instance=None,
    ):

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
            # log file path
            log_file_path=config.LogFilePath,
            # the tracing provider used
            tracing_provider_instance=tracing_provider_instance,
            # the path to the manifest file
            manifest_path=MANIFEST_PATH,
        )
