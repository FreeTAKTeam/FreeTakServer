from FreeTAKServer.components.core.abstract_component.facade import Facade
from FreeTAKServer.components.extended.emergency.emergency_constants import CONFIGURATION_PATH_TEMPLATE, ACTION_MAPPING_PATH
from . import domain

from .emergency_main import Emergency
from .emergency_logs import EmergencyLogs

class EmergencyFacade(Facade):
    
    state = None
    
    def __init__(self):
        # this if statement insures that EmergencyFacade is a singleton
        # this prevents reloading of the domain and other wasteful operations
        if self.state is None:
            self.emergency = Emergency()
            self.emergency_logs = EmergencyLogs()
            super().__init__(CONFIGURATION_PATH_TEMPLATE, domain, ACTION_MAPPING_PATH, self.emergency_logs)
            EmergencyFacade.state = self.__dict__
        else:
            self.__dict__ = EmergencyFacade.state
    
    def initialize(self, request, response):
        self.emergency.initialize(request, response)
        return super().initialize(request, response)
    
    def get_logs(self):
        self.emergency_logs.get_logs(**self.request.get_values())
        
    def emergency_alert(self):
        self.emergency.emergency_received(**self.request.get_values())

    def emergency_in_contact(self):
        self.emergency.emergency_received(**self.request.get_values())
        
    def emergency_geofence_breached(self):
        self.emergency.emergency_received(**self.request.get_values())
    
    def emergency_ring_the_bell(self):
        self.emergency.emergency_received(**self.request.get_values())

    def emergency_delete(self):
        self.emergency.emergency_delete(**self.request.get_values())
    
    def emergency_broadcast(self):
        self.emergency.emergency_broadcast(**self.request.get_values())    
    
    def emergency_broadcast_all(self):
        self.emergency.emergency_broadcast_all(**self.request.get_values())