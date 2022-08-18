from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory
from FreeTAKServer.components.core.cot_router.cot_router_constants import BASE_OBJECT_NAME, BASE_COT

class COTRouter(Controller):
    def __init__(self):
        pass
    
    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
    
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
    
    def cot_broadcast(self, model_object, **kwargs):
        self.response.set_values(kwargs)
        self.response.set_action('Broadcast')
        self.response.set_value('model_objects', [model_object])
    
    def cot_received(self, message, facade, logger, **kwargs):
        self.response.set_values(kwargs)
        
        logger.debug('received cot message')
        
        empty_model_object = facade.create_node(BASE_COT, BASE_OBJECT_NAME)
        
        request = ObjectFactory.get_new_instance('request')
        actionmapper = ObjectFactory.get_instance('actionMapper')
        response = ObjectFactory.get_new_instance('response')
        
        request.set_action('ParseCoT')
        request.set_value('message', message.xmlString)
        request.set_value('facade', facade)
        request.set_value('model_object', empty_model_object)
        
        actionmapper.process_action(request, response)
        
        self.response.set_value('model_object', response.get_value('model_object'))
        self.response.set_context('COT')
        self.response.set_action('CoTBroadcast')