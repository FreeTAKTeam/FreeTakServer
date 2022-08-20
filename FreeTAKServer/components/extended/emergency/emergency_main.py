from digitalpy.routing.controller import Controller
from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory

from FreeTAKServer.components.extended.emergency.emergency_rule_engine import EmergencyRuleEngine
from .domain import Event
from .emergency_constants import BASE_OBJECT_NAME, CREATE_EMERGENCY_TYPE, DELETE_EMERGENCY_TYPE, EMERGENCY_ON, EMERGENCY_OFF, EMERGENCY_ALERT
from lxml import etree

class Emergency(EmergencyRuleEngine):
    emergencies = {}
    
    def __init__(self):
        super().__init__()

    def accept_visitor(self, visitor):
        pass

    def initialize(self, request: Request, response: Response):
        self.request = request
        self.response = response
        
    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def emergency_broadcast(self, emergency: Event, **kwargs):
        """this method will broadcast a specific emergency
        
        Args:
            emergency_uid (str): the uid of the emergency to be broadcasted
        """
        try:
            self.request.get_value('logger').debug('broadcasting emergency %s', emergency.uid)
            
            self.response.set_values(kwargs)
            self.response.set_action('Broadcast')
            self.response.set_value('model_objects', [emergency])
        except Exception as error:
            self.request.get_value('logger').error('error broadcasting emergency %s', error)
    
    def _add_emergency_to_emergencies(self, emergency) -> None:
        """this method adds a new emergency to the list of emergencies
        
        Args:
            emergency (Event): the new emergency model object
        """
        try:
            emergency_uid = emergency.uid
            self.emergencies[emergency_uid] = emergency
            self.request.get_value('logger').debug('added emergency: %s to emergencies: %s', emergency_uid, self.emergencies)
        except Exception as error:
            self.request.get_value('logger').error('error adding emergency to emergencies %s', error)

    def _remove_emergency_from_emergencies(self, emergency)-> None:
        """this method removes the specified emergency from the list of emergencies

        Args:
            emergency (Event): the emergency delete model object
        """
        del self.emergencies[emergency.uid]
    
    def emergency_received(self, message, logger, facade, **kwargs):
        """this method is called to handle an emergency received
        Args:
            message (RawCoT): the RawCoT containing the emergency alert message
            logger (logging.Logger): the component logger instance
            facade (EmergencyFacade): the emergency facade used to access this method
        """
        try:
            self.response.set_values(kwargs)
            
            logger.info('emergency alert received')
            
            empty_model_object = facade.create_node(EMERGENCY_ALERT, BASE_OBJECT_NAME)
            
            request = ObjectFactory.get_new_instance('request')
            actionmapper = ObjectFactory.get_instance('actionMapper')
            response = ObjectFactory.get_new_instance('response')
            
            request.set_action('ParseCoT')
            request.set_value('message', message.xmlString)
            request.set_value('facade', facade)
            request.set_value('model_object', empty_model_object)
            
            actionmapper.process_action(request, response)
            
            emergency_object = response.get_value('model_object')
            
            self.apply_rules(emergency_object, **kwargs)
            
        except Exception as error:
            logger.error('exception in emergency alert: %s', error)
    
    def emergency_broadcast_all(self, **kwargs):
        """this method will broadcast all emergencies
        Args:
        """
        self.response.set_values(kwargs)
        self.response.set_action('Broadcast')
        self.response.set_value('model_objects', list(self.emergencies.values()))
    
    def emergency_delete(self, message, logger, facade, **kwargs):
        """this method is called to handle an emergency delete message
        Args:
            message (RawCoT): the RawCoT containing the emergency delete message
            logger (logging.Logger): the component logger instance
        """
        try:
            self.response.set_values(kwargs)
            
            logger.info('emergency delete received')
            
            empty_model_object = facade.create_node(EMERGENCY_OFF, BASE_OBJECT_NAME)
            
            request = ObjectFactory.get_new_instance('request')
            actionmapper = ObjectFactory.get_instance('actionMapper')
            response = ObjectFactory.get_new_instance('response')
            
            request.set_action('ParseCoT')
            request.set_value('message', message.xmlString)
            request.set_value('facade', facade)
            request.set_value('model_object', empty_model_object)
            
            actionmapper.process_action(request, response)
            
            emergency_object = response.get_value('model_object')
            
            self.apply_rules(emergency_object, **kwargs)
            
        except Exception as error:
            logger.error('exception in emergency delete: %s', error)
        
    def apply_rules(self, model_object, **kwargs):
        if self.create_emergency_alert_rule.matches(model_object.cot_attributes):
            self._add_emergency_to_emergencies(model_object)
            self.emergency_broadcast(model_object, **kwargs)
        
        elif self.create_emergency_contact_rule.matches(model_object.cot_attributes):
            self._add_emergency_to_emergencies(model_object)
            self.emergency_broadcast(model_object, **kwargs)
            
        elif self.create_emergency_ring_the_bell_rule.matches(model_object.cot_attributes):
            self.emergency_broadcast(model_object, **kwargs)
            
        elif self.create_emergency_geofence_breached_rule.matches(model_object.cot_attributes):
            self._add_emergency_to_emergencies(model_object)
            self.emergency_broadcast(model_object, **kwargs)
            
        elif self.delete_emergency_rule.matches(model_object.cot_attributes):
            self.emergency_broadcast(model_object, **kwargs)
            self._remove_emergency_from_emergencies(model_object)