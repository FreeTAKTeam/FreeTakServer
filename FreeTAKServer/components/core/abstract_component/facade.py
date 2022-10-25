from digitalpy.model.node import Node
from digitalpy.model.load_configuration import LoadConfiguration
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.routing.impl.default_action_mapper import DefaultActionMapper
from digitalpy.core.impl.default_event_manager import DefaultEventManager
from digitalpy.core.object_factory import ObjectFactory
from digitalpy.core.log_manager import LogManager
from digitalpy.core.impl.default_file_logger import DefaultFileLogger
from digitalpy.routing.controller import Controller
from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
import inspect
import sys
import importlib


class Facade(Controller):
    def __init__(
        self,
        action_mapping_path,
        internal_action_mapping_path,
        logger_configuration,
        component_name=None,
        type_mapping=None,
        action_mapper=None,
        base=object,
        request=None,
        response=None,
        configuration=None,
        configuration_path_template=None,
        **kwargs,
    ):
        super().__init__(
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
        self.base = base
        self.action_mapping_path = action_mapping_path
        self.internal_action_mapping_path = internal_action_mapping_path
        self.type_mapping = type_mapping
        self.action_mapper = action_mapper
        if component_name is not None:
            self.component_name = component_name
        else:
            self.component_name = self.__class__.__name__

        # define the logging
        self.log_manager = LogManager()
        DefaultFileLogger.set_base_logging_path(MainConfig.LogFilePath)
        self.log_manager.configure(
            DefaultFileLogger(
                name=self.component_name, config_file=logger_configuration
            )
        )
        self.logger = self.log_manager.get_logger()
        if configuration_path_template:
            self.config_loader = LoadConfiguration(configuration_path_template)
        else:
            self.config_loader = None

    def initialize(self, request, response):
        super().initialize(request, response)
        self.request.set_sender(self.__class__.__name__)

    def execute(self, method):
        self.request.set_value("logger", self.logger)
        self.request.set_value("config_loader", self.config_loader)
        response = self.execute_sub_action(self.request.get_action())
        self.response.set_values(response.get_values())

    def get_logs(self):
        self.log_manager.get_logs()

    def discover(self):
        pass

    def register(self, config: InifileConfiguration):
        config.add_configuration(self.action_mapping_path)
        internal_config = InifileConfiguration("")
        internal_config.add_configuration(self.internal_action_mapping_path)
        ObjectFactory.register_instance(
            f"{self.component_name.lower()}actionmapper",
            self.base.ActionMapper(
                ObjectFactory.get_instance("event_manager"), internal_config
            ),
        )
        self._register_type_mapping()

    def _register_type_mapping(self):
        """any component may or may not have a type mapping defined,
        if it does then it should be registered"""
        if self.type_mapping is not None:
            request = ObjectFactory.get_new_instance("request")
            request.set_action("RegisterMachineToHumanMapping")
            request.set_value("machine_to_human_mapping", self.type_mapping)

            actionmapper = ObjectFactory.get_instance("actionMapper")
            response = ObjectFactory.get_new_instance("response")
            actionmapper.process_action(request, response)

            request = ObjectFactory.get_new_instance("request")
            request.set_action("RegisterHumanToMachineMapping")
            # reverse the mapping and save the reversed mapping
            request.set_value(
                "human_to_machine_mapping", {k: v for v, k in self.type_mapping.items()}
            )

            actionmapper = ObjectFactory.get_instance("actionMapper")
            response = ObjectFactory.get_new_instance("response")
            actionmapper.process_action(request, response)

    def get_metrics(self):
        pass

    def get_health(self):
        pass

    def accept_visitor(self, node: Node, visitor, **kwargs):
        return node.accept_visitor(visitor)
