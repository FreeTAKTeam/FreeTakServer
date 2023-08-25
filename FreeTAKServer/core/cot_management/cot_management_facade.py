from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from digitalpy.core.zmanager.impl.async_action_mapper import AsyncActionMapper

from FreeTAKServer.core.cot_management.controllers.cot_management_repeater_controller import CotManagementRepeaterController
from FreeTAKServer.core.cot_management.controllers.cot_management_geo_object_controller import CotManagementGeoObjectController
from FreeTAKServer.core.cot_management.controllers.cot_management_general_controller import COTManagementGeneralController
from FreeTAKServer.core.cot_management.configuration.cot_management_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH
)
from . import base

class CotManagement(DefaultFacade):
    """Facade class for the this component. Responsible for handling all public
    routing. Forwards all requests to the internal router.
      WHY
      <ul>
      	<li><b>Isolation</b>: We can easily isolate our code from the complexity of
    a subsystem.</li>
      	<li><b>Testing Process</b>: Using Facade Method makes the process of testing
    comparatively easy since it has convenient methods for common testing tasks.
    </li>
      	<li><b>Loose Coupling</b>: Availability of loose coupling between the
    clients and the Subsystems.</li>
      </ul>
    """
    def __init__(
        self,
        sync_action_mapper,
        request,
        response,
        configuration,
        action_mapper: AsyncActionMapper=None,
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
        self.repeater_controller = CotManagementRepeaterController(request, response, sync_action_mapper, configuration)
        self.geo_object_controller = CotManagementGeoObjectController(request, response, sync_action_mapper, configuration)
        self.general_controller = COTManagementGeneralController(request, response, sync_action_mapper, configuration)
        self.injected_values["action_mapper"] = action_mapper

    def initialize(self, request, response):
        super().initialize(request, response)
        self.repeater_controller.initialize(request, response)
        self.geo_object_controller.initialize(request, response)
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
    def connection(self, *args, **kwargs):
        self.repeater_controller.connected_user(*args, **kwargs)

    @DefaultFacade.public
    def get_repeated_messages(self, *args, **kwargs):
        self.repeater_controller.get_repeated_messages(*args, **kwargs)

    def create_repeated_message(self, *args, **kwargs):
        self.repeater_controller.create_repeated_messages(*args, **kwargs)

    @DefaultFacade.public
    def delete_repeated_message(self, *args, **kwargs):
        self.repeater_controller.delete_repeated_message(*args, **kwargs)
    
    @DefaultFacade.public
    def create_geo_object(self, *args, **kwargs):
        self.geo_object_controller.create_geo_object(*args, **kwargs)

    @DefaultFacade.public
    def delete_geo_object(self, *args, **kwargs):
        self.geo_object_controller.delete_geo_object(*args, **kwargs)

    @DefaultFacade.public
    def default_cot_processor(self, *args, **kwargs):
        self.general_controller.handle_default_cot(**kwargs)