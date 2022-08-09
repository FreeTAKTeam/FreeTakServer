from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from FreeTAKServer.controllers.serializers.xml_serializer import XmlSerializer
from lxml import etree

class TargetXMLToModel_object:

    def __init__(self, model_object, domain):
        self.events = []
        self.model_object = model_object
        self.current_model_object = model_object
        self.domain = domain

    def start(self, tag: str, attrib: dict):
        if self.current_model_object.__class__.__name__.lower() != tag.lower():
            self.current_model_object = getattr(self.current_model_object, tag)

        for attr_name, attr_val in attrib.items():
            setattr(self.current_model_object, attr_name, attr_val)

    def end(self, tag):
        self.current_model_object = self.domain.get_parent(self.current_model_object)

    def data(self, data):
        setattr(self.current_model_object, 'INTAG', data)

    def comment(self, text):
        pass

    def close(self):
        return self.model_object
    
class COTParser(Controller):
    def __init__(self):
        pass
    
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def parse_objects_to_cots(self, model_objects, **kwargs):
        self.response.set_values(kwargs)
        messages = []
        for model_object in model_objects:
            self.response.set_values(kwargs)
            message = XmlSerializer().from_fts_object_to_format(model_object)
            messages.append(etree.tostring(message))
        self.response.set_value('messages', messages)
        
    def parse_cot_to_object(self, message, model_object, domain, **kwargs):
        self.response.set_values(kwargs)
        xml = message
        target_xml_to_model_object = TargetXMLToModel_object(model_object, domain)
        parser = etree.XMLParser(target = target_xml_to_model_object)
        model_object = etree.XML(xml, parser)
        self.response.set_value("model_object", model_object)