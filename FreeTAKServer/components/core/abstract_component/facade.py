from digitalpy.model.node import Node
from digitalpy.model.load_configuration import LoadConfiguration
from digitalpy.config.impl.inifile_configuration import InifileConfiguration
from digitalpy.routing.impl.default_action_mapper import DefaultActionMapper
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
        config_path_template,
        domain,
        action_mapping_path,
        logger_configuration,
        component_name=None,
        type_mapping=None,
        controllers=[],
        **kwargs
    ):
        self.controllers = controllers
        # dynamically initialize all controllers in
        controller_modules = [
            member
            for member in inspect.getmembers(
                importlib.import_module(
                    importlib.import_module(self.__module__).__package__
                )
            )
            if inspect.ismodule(member)
        ]
        for controller_module in controller_modules:
            controller_classes = [
                m[0]
                for m in inspect.getmembers(controller_module, inspect.isclass)
                if m[1].__module__ == "my_module"
            ]
            for controller_class in controller_classes:
                controller_instance = controller_class(**kwargs)
                self.controllers.append(controller_instance)
                setattr(self, controller_class.__class__.__name__, controller_instance)

        if component_name is not None:
            self.component_name = component_name
        else:
            self.component_name = self.__class__.__name__

        self.config_loader = LoadConfiguration(config_path_template)
        self.domain = domain
        self.action_mapping_path = action_mapping_path
        self.type_mapping = type_mapping
        self.log_manager = LogManager()
        DefaultFileLogger.set_base_logging_path(MainConfig.LogFilePath)
        self.log_manager.configure(
            DefaultFileLogger(
                name=self.component_name, config_file=logger_configuration
            )
        )
        self.logger = self.log_manager.get_logger()

    def initialize(self, request, response):
        super().initialize(request, response)
        # initialize all used controllers
        for controller in self.controllers:
            controller.initialize(request, response)

        self.request.set_sender(self.__class__.__name__)

    def execute(self, method=None):
        self.request.set_value("logger", self.logger)
        getattr(self, method)(**self.request.get_values())

    def get_logs(self):
        self.log_manager.get_logs()

    def discover(self):
        pass

    def register(self, config: InifileConfiguration):
        config.add_configuration(self.action_mapping_path)
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

    def add_child(self, node: Node, child, **kwargs):
        return node.add_child(child)

    def create_node(self, message_type, object_class_name, **kwargs):
        configuration = self.config_loader.find_configuration(message_type)
        object_class = getattr(self.domain, object_class_name)
        object_class_instance = object_class(configuration, self.domain)
        return object_class_instance

    def delete_child(self, node: Node, child_id, **kwargs):
        return node.delete_child(child_id)

    def get_children_ex(
        self,
        id,
        node: Node,
        children_type,
        values,
        properties,
        use_regex=True,
        **kwargs
    ):
        return node.get_children_ex(
            id, node, children_type, values, properties, use_regex
        )

    def get_first_child(
        self, node: Node, child_type, values, properties, use_regex=True, **kwargs
    ):
        return node.get_first_child(child_type, values, properties, use_regex)

    def get_next_sibling(self, node, **kwargs):
        return node.get_next_sibling()

    def get_num_children(self, node: Node, children_type=None, **kwargs):
        return node.get_num_children(children_type)

    def get_num_parents(self, node: Node, parent_types=None, **kwargs):
        return node.get_num_parents(parent_types)

    def get_previous_sibling(self, node: Node, **kwargs):
        return node.get_previous_sibling()

    def get_parent(self, node: Node, **kwargs):
        self.response.set_value("parent", node.get_parent())
