from digitalpy.core.main.controller import Controller
from digitalpy.core.parsing.load_configuration import LoadConfiguration
from digitalpy.core.domain.node import Node


class Domain(Controller):
    def __init__(self, config_path_template, domain, **kwargs):
        super().__init__(**kwargs)
        self.config_loader = LoadConfiguration(config_path_template)
        self.domain = domain

    def execute(self, method=None):
        return getattr(self, method)(**self.request.get_values())

    def add_child(self, node: Node, child, **kwargs):
        return node.add_child(child)

    def create_node(self, message_type, object_class_name, **kwargs):
        configuration = self.config_loader.find_configuration(message_type)
        object_class = getattr(self.domain, object_class_name)
        object_class_instance = object_class(configuration, self.domain)
        self.response.set_value("model_object", object_class_instance)

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
