from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.components.core.domain.configuration.domain_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
)

from .controllers.dict_to_node_controller import DictToNodeController
from .controllers.domain import Domain as DomainController
from . import base

config = MainConfig.instance()


class Domain(DefaultFacade):
    """This is the facade class for the domain component, it is responsible
    for handling all public routing and forwards all requests to the internal routing
    """

    def __init__(
        self,
        sync_action_mapper,
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
            action_mapper=sync_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # log file path
            log_file_path=config.LogFilePath,
            # the tracing provider used
            tracing_provider_instance=tracing_provider_instance,
            # the path to the manifest file
            manifest_path=MANIFEST_PATH,
        )
        self.dict_to_node_controller = DictToNodeController(request, response, sync_action_mapper, configuration)
        self.domain_controller = DomainController(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        super().initialize(request, response)
        self.dict_to_node_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)

    def execute(self, method):
        try:
            if hasattr(self, method):
                getattr(self, method)(**self.request.get_values())
            else:
                self.request.set_value("logger", self.logger)
                self.request.set_value("config_loader", self.config_loader)
                self.request.set_value("tracer", self.tracer)
                response = self.execute_sub_action(self.request.get_action())
                self.response.set_values(response.get_values())
        except Exception as e:
            self.logger.fatal(str(e))

    @DefaultFacade.public
    def convert_dict_to_node(self, *args, **kwargs):
        self.dict_to_node_controller.convert_dict_to_node(*args,**kwargs)

    @DefaultFacade.public
    def create_node(self, *args, **kwargs):
        self.domain_controller.create_node(*args, **kwargs)
    
    @DefaultFacade.public
    def get_node_parent(self, *args, **kwargs):
        self.domain_controller.get_parent(*args, **kwargs)