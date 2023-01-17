from typing import Union
from digitalpy.core.main.controller import (
    Controller,
)
from digitalpy.core.domain.node import Node
from copy import deepcopy
from lxml.etree import Element  # pylint: disable=no-name-in-module
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

    def convert_xml_to_dict(self, message: str, **kwargs):
        """converts the provided xml string to a dictionary

        Args:
            message (str): xml string to be converted to a dictionary
        """
        self.response.set_value("dict", xmltodict.parse(message))

    def convert_node_to_xml(self, node, **kwargs):
        """converts the provided node to an xml string

        Args:
            node (Node): the node to be serialized to xml
        """
        self.response.set_value(
            "message", self._serialize_node(node, node.__class__.__name__.lower())
        )

    def _serialize_node(
        self, node: Node, tag_name: str, level=0
    ) -> Union[str, Element]:
        """the body of the serialization function recursively serializes each node class

        Args:
            node (Node): the root node class to be serialized
            tag_name (str): the name of the root node class to be serialized
            level (int, optional): _description_. Defaults to 0.

        Returns:
            Union[str, Element]: the original call to this method returns a string representing the xml
                the Element is only returned in the case of recursive calls
        """
        xml = Element(tag_name)
        # handles text data within tag
        if hasattr(node, "text"):
            xml.text = node.text

        for attribName in node.get_all_properties():
            # below line is required because get_all_properties function returns only cot property names
            value = getattr(node, attribName)

            if value == None:
                continue

            elif isinstance(value, list):
                for element in value:
                    tagElement = self._serialize_node(
                        element, attribName, level=level + 1
                    )
                    # TODO: modify so double underscores are handled differently
                    try:
                        if attribName[0] == "_":
                            tagElement.tag = "_" + tagElement.tag
                            xml.append(tagElement)
                    except:
                        pass
                    else:
                        xml.append(tagElement)

            else:
                # TODO: modify so double underscores are handled differently
                # handles instances in which attribute name begins with double underscore
                try:
                    if attribName[0] == "_":
                        xml.attrib["_" + attribName] = value
                except:
                    pass
                else:
                    xml.attrib[attribName] = str(value)

        for child in node.get_children():
            tagElement = self._serialize_node(child, child.get_type(), level=level + 1)
            # TODO: modify so double underscores are handled differently
            try:
                if attribName[0] == "_":
                    tagElement.tag = "_" + tagElement.tag
                    xml.append(tagElement)
            except:
                pass
            else:
                xml.append(tagElement)
        
        if hasattr(node, "xml_string"):
            # this method combines the xml object parsed from
            # the model object with the xml_string found in the node
            # directly, giving priority to the xml object parsed from the model object
            xml = self._xml_merge(node.xml_string, xml)
        if level == 0:
            return etree.tostring(xml)
        else:
            return xml

    def _xml_merge(self, a, b):
        """credits: https://gist.github.com/dirkjot/bd25b037b33bba6187e99d76792ceb90
        this function merges two xml etree elements

        Args:
            a (_type_): _description_
            b (_type_): _description_
        """

        def inner(a_parent, b_parent):
            for bchild in b_parent:
                achild = a_parent.xpath("./" + bchild.tag)
                if not achild:
                    a_parent.append(bchild)
                elif bchild.getchildren():
                    inner(achild[0], bchild)

        res = deepcopy(a)
        inner(res, b)
        return res
