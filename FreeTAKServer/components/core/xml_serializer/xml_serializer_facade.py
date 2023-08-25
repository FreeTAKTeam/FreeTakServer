from FreeTAKServer.components.core.xml_serializer.controllers.xml_serialization_controller import XMLSerializationController
from digitalpy.core.component_management.impl.default_facade import DefaultFacade
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.components.core.xml_serializer.configuration.xml_serializer_constants import (
    ACTION_MAPPING_PATH,
    TYPE_MAPPINGS,
    LOGGING_CONFIGURATION_PATH,
    INTERNAL_ACTION_MAPPING_PATH,
    MANIFEST_PATH,
)
from . import base

config = MainConfig.instance()


class XmlSerializer(DefaultFacade):
    """Facade class for the Component component. Responsible for handling all public routing.
    Forwards all requests to the internal router.
    """

    def __init__(
        self,
        xml_serializer_action_mapper,
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
            # the type mapping in dictionary form
            type_mapping=TYPE_MAPPINGS,
            # the path to the logger configuration
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            # the package containing the base classes
            base=base,
            # the component specific action mapper (passed by constructor)
            action_mapper=xml_serializer_action_mapper,
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
        self.serialization_controller = XMLSerializationController(request, response, xml_serializer_action_mapper, configuration)

    def initialize(self, request, response):
        super().initialize(request, response)
        self.serialization_controller.initialize(request, response)

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
    def convert_dict_to_xml(self, *args, **kwargs):
        self.serialization_controller.convert_dict_to_xml(*args,**kwargs)

    @DefaultFacade.public
    def convert_xml_to_dict(self, *args, **kwargs):
        self.serialization_controller.convert_xml_to_dict(*args,**kwargs)

    @DefaultFacade.public
    def convert_node_to_xml(self, *args, **kwargs):
        self.serialization_controller.convert_node_to_xml(*args,**kwargs)