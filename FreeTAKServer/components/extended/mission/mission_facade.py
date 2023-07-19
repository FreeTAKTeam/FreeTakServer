from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.extended.mission.controllers.mission_subscription_controller import MissionSubscriptionController
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from .controllers.mission_general_controller import MissionGeneralController

from .configuration.mission_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH
)
from . import base

class Mission(DefaultFacade):
    """facade class managing inbound and outbound traffic from the component to the outside world
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
        self.general_controller = MissionGeneralController(request, response, sync_action_mapper, configuration)
        self.persistence_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)
        self.subscription_controller = MissionSubscriptionController(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        super().initialize(request, response)
        self.general_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)
        self.subscription_controller.initialize(request, response)

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
    
    def register(self, *args, **kwargs):
        super().register(*args, **kwargs)
        self.persistence_controller.create_default_permissions()
        self.persistence_controller.create_default_roles()
        
    @DefaultFacade.public
    def put_mission(self, *args, **kwargs):
        self.general_controller.put_mission(*args, **kwargs)

    @DefaultFacade.public
    def create_mission_content(self, *args, **kwargs):
        self.general_controller.create_mission_content(*args, **kwargs)
        
    @DefaultFacade.public
    def get_missions(self, *args, **kwargs):
        self.general_controller.get_missions(*args, **kwargs)
        
    @DefaultFacade.public
    def get_mission(self, *args, **kwargs):
        self.general_controller.get_mission(*args, **kwargs)
        
    @DefaultFacade.public
    def get_mission_logs(self, *args, **kwargs):
        self.general_controller.get_mission_logs(*args, **kwargs)
        
    @DefaultFacade.public
    def get_mission_subscriptions(self, *args, **kwargs):
        self.subscription_controller.get_mission_subscriptions(*args, **kwargs)
        
    @DefaultFacade.public
    def add_mission_contents(self, *args, **kwargs):
        self.general_controller.add_contents_to_mission(*args, **kwargs)