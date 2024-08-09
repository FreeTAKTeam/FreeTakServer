from lxml import etree
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from .xml_serializer import XmlSerializer
from .xml_element import ExtendedElement
from FreeTAKServer.model.FTSModel.fts_protocol_object import FTSProtocolObject
from ...domain import Domain

class XMLSerializationOrchestrator(Controller):
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
    ):
        super().__init__(
            request=request,
            response=response,
            action_mapper=sync_action_mapper,
            configuration=configuration,
        )
        self.domain_controller = Domain(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        super().initialize(request, response)
        self.domain_controller.initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response

    def node_to_xml(self, model_objects, **kwargs):
        self.response.set_values(kwargs)
        messages = []
        for model_object in model_objects:
            # TODO: Direct calls shouldnt be made!!!!! this must be changed ASAP
            message = XmlSerializer().serialize_model_to_CoT(model_object)
            messages.append(message)
        self.response.set_value("messages", messages)

    def xml_to_node(self, message, model_object, **kwargs):
        self.response.set_values(kwargs)
        xml = message.xmlString
        target_xml_to_model_object = TargetXMLToModel_object(
            model_object, self._get_parent
        )
        parser = etree.XMLParser(target=target_xml_to_model_object)
        model_object = etree.XML(xml, parser)
        self.response.set_value("model_object", model_object)

    def _get_parent(self, node, type=""):
        return self.domain_controller.get_parent(node)

class TargetXMLToModel_object:
    def __init__(self, model_object, parent_getter):
        self.internal_parser = etree.XMLParser()
        lookup = etree.ElementDefaultClassLookup(element=ExtendedElement)
        self.internal_parser.set_element_class_lookup(lookup)
        self.model_object = model_object
        self.current_model_object = model_object
        self.parent_getter = parent_getter

    def start(self, tag: str, attrib: dict):

        # if the current model object is an etree element then add the current tag
        # as a sub element of the parent and set the sub element as the new root
        if isinstance(self.current_model_object, etree._Element):
            self.current_model_object = etree.SubElement(
                self.current_model_object, tag, attrib
            )

        # otherwise the parent should be a model object which all subclass from FTSProtocolObject
        elif isinstance(self.current_model_object, FTSProtocolObject):

            # if the current_model_object is not the current tag then
            # it must have a child which is the model equivalent to the
            # tag get this model equivalent
            if self.current_model_object.__class__.__name__.lower() != tag.lower():

                self.current_model_object = self.current_model_object.cot_attributes[
                    tag
                ]

            if hasattr(self.current_model_object, "xml_string"):
                etree_element = self.internal_parser.makeelement(tag, attrib)
                etree_element.set_parent(
                    self.parent_getter(
                        self.current_model_object, self.model_object.type
                    )
                )
                setattr(self.current_model_object, "xml_string", etree_element)
                self.current_model_object = etree_element
                return

            for attr_name, attr_val in attrib.items():
                self.current_model_object.cot_attributes[attr_name] = attr_val

        else:
            raise TypeError("an invalid type was passed as the current_model_object")

    def end(self, tag):
        # in the case that the current_model_object is an etree element then use the getparent() method
        if isinstance(self.current_model_object, etree._Element):
            self.current_model_object = self.current_model_object.getparent()

        elif isinstance(self.current_model_object, FTSProtocolObject):
            self.current_model_object = self.parent_getter(
                self.current_model_object, self.model_object.type
            )

        else:
            raise TypeError("an invalid type was passed as the current_model_object")

    def data(self, data):
        if isinstance(self.current_model_object, FTSProtocolObject):
            self.current_model_object.text += data
        elif isinstance(self.current_model_object, etree._Element):
            self.current_model_object.text = data

    def comment(self, text):
        pass

    def close(self):
        return self.model_object
