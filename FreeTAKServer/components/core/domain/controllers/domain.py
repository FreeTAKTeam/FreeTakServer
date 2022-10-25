from digitalpy.routing.action_mapper import ActionMapper
from digitalpy.config.configuration import Configuration
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.model.load_configuration import Configuration
from digitalpy.model.node import Node
from digitalpy.routing.controller import Controller

from .. import domain


class Domain(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        domain_action_mapper: ActionMapper,
        configuration: Configuration,
        **kwargs,
    ):
        super().__init__(request, response, domain_action_mapper, configuration)
        self.domain = domain

    def execute(self, method=None):
        return getattr(self, method)(**self.request.get_values())

    def add_child(self, node: Node, child, **kwargs):
        return node.add_child(child)

    def create_node(self, configuration: Configuration, object_class_name, **kwargs):
        object_class = getattr(self.domain, object_class_name)
        object_class_instance = object_class(configuration, self.domain)
        self.response.set_value("model_object", object_class_instance)
        self.request.set_value("model_object", object_class_instance)
        if self.request.get_value("source_format") and self.request.get_value(
            "target_format"
        ):
            self.execute_sub_action("Serialize")

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
        **kwargs,
    ):
        self.response.set_value(
            "children",
            node.get_children_ex(
                id, node, children_type, values, properties, use_regex
            ),
        )

    def get_first_child(
        self, node: Node, child_type, values, properties, use_regex=True, **kwargs
    ):
        self.response.set_value(
            "first_child",
            node.get_first_child(child_type, values, properties, use_regex),
        )

    def get_next_sibling(self, node, **kwargs):
        self.response.set_value("next_sibling", node.get_next_sibling())

    def get_num_children(self, node: Node, children_type=None, **kwargs):
        self.response.set_value("num_children", node.get_num_children(children_type))

    def get_num_parents(self, node: Node, parent_types=None, **kwargs):
        self.response.set_value("num_parents", node.get_num_parents(parent_types))

    def get_previous_sibling(self, node: Node, **kwargs):
        self.response.set_value("previous_sibling", node.get_previous_sibling())

    def get_parent(self, node: Node, **kwargs):
        self.response.set_value("parent", node.get_parent())
