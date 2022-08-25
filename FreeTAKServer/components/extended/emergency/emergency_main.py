from digitalpy.routing.request import Request
from digitalpy.routing.response import Response
from digitalpy.core.object_factory import ObjectFactory

from FreeTAKServer.components.extended.emergency.emergency_rule_engine import EmergencyRuleEngine
from .domain import Event
from .emergency_constants import BASE_OBJECT_NAME, EMERGENCY_OFF, EMERGENCY_ALERT

class EmergencyMain(EmergencyRuleEngine):
    emergencies = {}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            self.request.get_value('logger').debug(f'broadcasting emergency {emergency.uid}')
            
            self.response.set_values(kwargs)
            self.response.set_action('Broadcast')
            self.response.set_value('model_objects', [emergency])
        except Exception as error:
            self.request.get_value('logger').error(f'error broadcasting emergency {error}')
    
    def _add_emergency_to_emergencies(self, emergency) -> None:
        """this method adds a new emergency to the list of emergencies
        
        Args:
            emergency (Event): the new emergency model object
        """
        try:
            emergency_uid = emergency.uid
            self.emergencies[emergency_uid] = emergency
            self.request.get_value('logger').debug(f'added emergency: {emergency_uid} to emergencies: {self.emergencies}')
        except Exception as error:
            self.request.get_value('logger').error(f'error adding emergency to emergencies {error}')

    def _remove_emergency_from_emergencies(self, emergency)-> None:
        """this method removes the specified emergency from the list of emergencies

        Args:
            emergency (Event): the emergency delete model object
        """
        del self.emergencies[emergency.uid]
    
    def emergency_received(self, logger, **kwargs):
        """this method is called to handle an emergency received
        Args:
            message (RawCoT): the RawCoT containing the emergency alert message
            logger (logging.Logger): the component logger instance
        """
        try:
            self.response.set_values(kwargs)
            
            logger.info('emergency alert received')
            
            facade = ObjectFactory.get_instance(self.request.get_sender())
            
            empty_model_object = facade.create_node(EMERGENCY_ALERT, BASE_OBJECT_NAME)
            
            self.request.set_value('model_object', empty_model_object)
            
            self.request.set_value('message', self.request.get_value('message').xmlString)
            
            emergency_object = self.execute_sub_action('ParseCoT').get_value('model_object')
            
            self.apply_rules(emergency_object, **kwargs)
            
        except Exception as error:
            logger.error(f'exception in emergency alert: {error}')
    
    def emergency_broadcast_all(self, **kwargs):
        """this method will broadcast all emergencies
        Args:
        """
        self.response.set_values(kwargs)
        self.response.set_action('Broadcast')
        self.response.set_value('model_objects', list(self.emergencies.values()))
    
    def emergency_delete(self, message, logger, **kwargs):
        """this method is called to handle an emergency delete message
        Args:
            message (RawCoT): the RawCoT containing the emergency delete message
            logger (logging.Logger): the component logger instance
        """
        try:
            self.response.set_values(kwargs)
            
            logger.info('emergency delete received')
            
            facade = ObjectFactory.get_instance(self.request.get_sender())
            
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
            logger.error(f'exception in emergency delete: {error}')
        
    def apply_rules(self, model_object, **kwargs):
        if self.create_emergency_alert_rule.matches(model_object):
            self._add_emergency_to_emergencies(model_object)
            self.emergency_broadcast(model_object, **kwargs)
        
        elif self.create_emergency_contact_rule.matches(model_object):
            self._add_emergency_to_emergencies(model_object)
            self.emergency_broadcast(model_object, **kwargs)
            
        elif self.create_emergency_ring_the_bell_rule.matches(model_object):
            self.emergency_broadcast(model_object, **kwargs)
            
        elif self.create_emergency_geofence_breached_rule.matches(model_object):
            self._add_emergency_to_emergencies(model_object)
            self.emergency_broadcast(model_object, **kwargs)
            
        elif self.delete_emergency_rule.matches(model_object):
            self.emergency_broadcast(model_object, **kwargs)
            self._remove_emergency_from_emergencies(model_object)