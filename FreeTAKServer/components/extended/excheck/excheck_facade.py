from FreeTAKServer.components.extended.excheck.controllers.excheck_checklist_controller import ExCheckChecklistController
from FreeTAKServer.components.extended.excheck.controllers.excheck_template_controller import ExCheckTemplateController
from FreeTAKServer.components.extended.excheck.controllers.excheck_notification_controller import ExCheckNotificationController
from digitalpy.core.component_management.impl.default_facade import DefaultFacade


from .configuration.excheck_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
    CONFIGURATION_PATH_TEMPLATE,
    LOG_FILE_PATH
)
from . import base

class Excheck(DefaultFacade):
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
        self.template_controller = ExCheckTemplateController(request, response, sync_action_mapper, configuration)
        self.checklist_controller = ExCheckChecklistController(request, response, sync_action_mapper, configuration)
        self.notification_controller = ExCheckNotificationController(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        super().initialize(request, response)
        self.template_controller.initialize(request, response)
        self.checklist_controller.initialize(request, response)
        self.notification_controller.initialize(request, response)
        
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
        self.template_controller.create_template_mission()

    @DefaultFacade.public
    def create_template(self, *args, **kwargs):
        return self.template_controller.create_template(*args, **kwargs)

    @DefaultFacade.public
    def get_all_templates(self, *args, **kwargs):
        return self.template_controller.get_all_templates(*args, **kwargs)
    
    @DefaultFacade.public
    def get_template(self, *args, **kwargs):
        return self.template_controller.get_template(*args, **kwargs)

    @DefaultFacade.public
    def start_checklist(self, *args, **kwargs):
        return self.checklist_controller.start_checklist(*args, **kwargs)
    
    @DefaultFacade.public
    def update_checklist_task(self, *args, **kwargs):
        return self.checklist_controller.update_checklist_task(*args, **kwargs)
    
    @DefaultFacade.public
    def checklist_update_notification(self, *args, **kwargs):
        return self.notification_controller.send_task_update_notification(*args, **kwargs)

    @DefaultFacade.public
    def get_checklist(self, *args, **kwargs):
        return self.checklist_controller.get_checklist(*args, **kwargs)

    @DefaultFacade.public
    def get_checklists(self, *args, **kwargs):
        return self.checklist_controller.get_all_checklists(*args, **kwargs)
    
    @DefaultFacade.public
    def get_checklist_task(self, *args, **kwargs):
        return self.checklist_controller.get_checklist_task(*args, **kwargs)

    @DefaultFacade.public
    def get_checklist_mission(self, *args, **kwargs):
        return self.checklist_controller.get_checklist_mission(*args, **kwargs)

    @DefaultFacade.public
    def add_checklist_to_mission(self, *args, **kwargs):
        return self.checklist_controller.add_checklist_to_mission(*args, **kwargs)