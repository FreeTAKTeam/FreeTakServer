from digitalpy.core.main.controller import Controller
from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.domain.node import Node


class DictToNodeController(Controller):
    def execute(self, method=None):
        return getattr(self, method)(**self.request.get_values())

    def convert_dict_to_node(
        self,
        dictionary: dict,
        model_object: Node,
        tracer: Tracer,
        object_class_name,
        **kwargs
    ):
        """fill the node object with the values from the dictionary

        Args:
            dictionary (dict): a dictionary containing key value pairs which match to the given node attributes.
            model_object (Node): a node object instance with null attributes.
            tracer (Tracer, optional): a tracer object used for logging which should be passed by the facade. Defaults to None.
        """
        with tracer.start_as_current_span("convert_dict_to_node") as span:
            try:
                span.add_event(
                    "serializing " + str(dictionary) + " to node " + str(model_object)
                )
                self.response.set_value(
                    "model_object",
                    self.serialize(dictionary[object_class_name.lower()], model_object),
                )
                span.add_event("serialization completed successfully")
            except Exception as ex:
                span.record_exception(ex)

    def serialize(self, dictionary, node):
        """recursively serialize a single layer of the given dictionary
        to a node object until a nested dictionary is found"""
        for key, value in dictionary.items():
            self.add_value_to_node(key, value, node)
        return node

    def add_value_to_node(self, key, value, node):
        """add a value to a node object"""

        if isinstance(value, dict):
            self.serialize(value, getattr(node, key))

        elif isinstance(value, list):
            for l_item in value:
                self.add_value_to_node(key, l_item, node)
        else:
            setattr(node, key.strip("@"), value)
