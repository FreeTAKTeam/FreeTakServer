from digitalpy.core.main.controller import Controller
from digitalpy.core.telemetry.tracer import Tracer
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.domain.node import Node
from lxml import etree

class DictToNodeController(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ) -> None:
        super().__init__(request, response, sync_action_mapper, configuration)

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
            span.add_event(
                "serializing " + str(dictionary) + " to node " + str(model_object)
            )
            self.response.set_value(
                "model_object",
                self.serialize(dictionary[object_class_name.lower()], model_object),
            )
            span.add_event("serialization completed successfully")

    def serialize(self, dictionary, node):
        """recursively serialize a single layer of the given dictionary
        to a node object until a nested dictionary is found"""
        for key, value in dictionary.items():
            self.add_value_to_node(key, value, node)
        return node

    def add_value_to_node(self, key, value, node):
        """add a value to a node object"""
        if key == "#text":
            setattr(node, "INTAG", value)

        elif not hasattr(node, key.strip("@")):
            self.handle_missing_attribute(key, value, node)

        # this and ensures that the value is absoloutly a Node type instead of an expected list with only value, ex. a pm to one user would be a single object in the dict representation
        # however it's expected to be a list
        elif isinstance(value, dict) and isinstance(getattr(node, key, None), Node):
            self.serialize(value, getattr(node, key))

        elif isinstance(value, list) and isinstance(getattr(node, key, None), list):
            for l_item in value:
                self.add_value_to_node(key, l_item, node)

        elif isinstance(getattr(node, key, None), list):
            self.serialize(value, getattr(node, key)[0])

        else:
            setattr(node, key.strip("@"), value)

    def handle_missing_attribute(self, key, value, node):
        """given the dynamic and expanding domain of the CoT standard there is always a risk of undocumented or new attributes or tags 
        appearing in a given cot which does not yet exist in the domain, in these cases the keys and values will be converted to xml strings
        and added to the cot_node

        Args:
            key (str): attribute or tag
            value (Union[str, dict, List]): object or objects of the attribute/tag
            node (str): model object to store xml_string
        """
        # this if case handles undefined nested objects
        if isinstance(value, dict):
            self.request.set_value("xml_dict", {key: value})
            response = self.execute_sub_action("DictToXML")
            elem = etree.fromstring(response.get_value("xml").encode())
            node.xml.append(elem)
        elif isinstance(value, list):
            for l_item in value:
                self.add_value_to_node(key, l_item, node)
                response = self.execute_sub_action("DictToXML")
                elem = etree.Element(key, response.get_value("message"))
                node.xml.append(elem)
                
        elif value is not None:
            node.xml.attrib[key] = value