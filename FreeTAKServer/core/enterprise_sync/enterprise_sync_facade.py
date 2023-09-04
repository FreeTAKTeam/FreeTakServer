from FreeTAKServer.core.enterprise_sync.controllers.enterprise_sync_general_controller import EnterpriseSyncGeneralController
from digitalpy.core.component_management.impl.default_facade import DefaultFacade


from .configuration.enterprise_sync_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH
)
from . import base

class EnterpriseSync(DefaultFacade):
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
            # the general action mapper (passed by constructor)
            action_mapper=sync_action_mapper,
            # the request object (passed by constructor)
            request=request,
            # the response object (passed by constructor)
            response=response,
            # the configuration object (passed by constructor)
            configuration=configuration,
            # log file path
            log_file_path= LOG_FILE_PATH,
            # the tracing provider used
            tracing_provider_instance=tracing_provider_instance,
            # the template for the absolute path to the model object definitions
            configuration_path_template=CONFIGURATION_PATH_TEMPLATE,
            # the path to the manifest file
            manifest_path=MANIFEST_PATH,
        )
        self.general_controller = EnterpriseSyncGeneralController(request, response, sync_action_mapper, configuration)
  
    def initialize(self, request, response):
        super().initialize(request, response)
        self.general_controller.initialize(request, response)

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
    def save_enterprise_sync_data(self, *args, **kwargs):
        self.general_controller.save_enterprise_sync_data(*args, **kwargs)
    
    @DefaultFacade.public
    def get_enterprise_sync_data(self, *args, **kwargs):
        self.general_controller.get_enterprise_sync_data(*args, **kwargs)

    @DefaultFacade.public
    def get_multiple_enterprise_sync_data(self,*args, **kwargs):
        self.general_controller.get_multiple_enterprise_sync_data(*args, **kwargs)

    @DefaultFacade.public
    def get_enterprise_sync_metadata(self,*args, **kwargs):
        self.general_controller.get_enterprise_sync_metadata(*args, **kwargs)

    @DefaultFacade.public
    def get_multiple_enterprise_sync_metadata(self,*args, **kwargs):
        self.general_controller.get_multiple_enterprise_sync_metadata(*args, **kwargs)

    @DefaultFacade.public
    def update_enterprise_sync_metadata(self, *args, **kwargs):
        self.general_controller.update_enterprise_sync_metadata(*args, **kwargs)
        
    @DefaultFacade.public
    def update_enterprise_sync_data(self, *args, **kwargs):
        self.general_controller.update_enterprise_sync_data(*args, **kwargs)

    @DefaultFacade.public
    def get_all_enterprise_sync_metadata(self, *args, **kwargs):
        self.general_controller.get_all_enterprise_sync_metadata(*args, **kwargs)

    @DefaultFacade.public
    def delete_enterpire_sync_data(self, *args, **kwargs):
        self.general_controller.delete_enterprise_sync_data(*args, **kwargs)