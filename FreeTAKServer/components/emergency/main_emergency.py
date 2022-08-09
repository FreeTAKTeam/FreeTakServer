from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory
from .emergency_constants import BASE_OBJECT_NAME, CREATE_EMERGENCY_TYPE, DELETE_EMERGENCY_TYPE, EMERGENCY_ON, EMERGENCY_OFF
from .emergency_domain import _EmergencyDomain
from lxml import etree

class Emergency(Controller):
    emergencies = {}
    
    def __init__(self):
        pass

    def accept_visitor(self, visitor):
        pass

    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def _get_emergency_type(self, emergency_string):
        return etree.fromstring(emergency_string).attrib["type"]
    
    def emergency_received(self, emergency, **kwargs):
        self.response.set_values(kwargs)
        
        domain = _EmergencyDomain()
        
        request = ObjectFactory.get_new_instance('request')
        request.set_action('ParseCoT')
        request.set_value('message', emergency.xmlString)
        request.set_value('domain', domain)
        
        actionmapper = ObjectFactory.get_instance('actionMapper')
        response = ObjectFactory.get_new_instance('response')

        if self._get_emergency_type(emergency.xmlString) == CREATE_EMERGENCY_TYPE:
            model_object = domain.create_node(EMERGENCY_ON, BASE_OBJECT_NAME)
            request.set_value('model_object', model_object)
            actionmapper.process_action(request, response)
            
            self.create_emergency(model_object)

        elif self._get_emergency_type(emergency.xmlString) == DELETE_EMERGENCY_TYPE:
            model_object = domain.create_node(EMERGENCY_OFF, BASE_OBJECT_NAME)
            request.set_value('model_object', model_object)
            actionmapper.process_action(request, response)

            self.delete_emergency(model_object.uid)

        self.response.set_value('message', response.get_value('model_object'))

    def create_emergency(self, emergency_model_object, **kwargs):
        self.response.set_values(kwargs)
        self.emergencies[emergency_model_object.uid] = emergency_model_object
        
    def delete_emergency(self, emergency_uid, **kwargs):
        self.response.set_values(kwargs)
        del self.emergencies[emergency_uid]
        
    def broadcast_emergencys(self, **kwargs):
        self.response.set_values(kwargs)
        self.response.set_action('Broadcast')
        self.response.set_value('model_objects', list(self.emergencies.values()))