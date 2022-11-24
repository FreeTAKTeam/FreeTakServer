from digitalpy.routing.controller import (
    Controller,
)
from lxml import etree
import xmltodict
from ..configuration.xml_serializer_constants import (
    XML_SERIALIZER_BUSINESS_RULES_PATH,
    XML_SERIALIZER,
    BASE_OBJECT_NAME,
)


class XMLSerializationController(Controller):
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def convert_xml_to_dict(self, message, **kwargs):
        """converts the provided xml to a dictionary"""
        self.response.set_values(kwargs)
        self.response.set_value("dict", xmltodict.parse(message))
        return self.response

    def convert_node_to_xml(self, node, **kwargs):
        """converts the provided node to an xml string"""
        pass
