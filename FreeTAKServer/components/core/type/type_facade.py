from FreeTAKServer.components.core.abstract_component.facade import Facade
from FreeTAKServer.components.extended.emergency.emergency_constants import CONFIGURATION_PATH_TEMPLATE, ACTION_MAPPING_PATH
from .type_main import TypeMain
from .type_logs import TypeLogs
from .mapping_strategies import MemoryMapping

class TypeFacade(Facade):
    
    state = None
    
    def __init__(self):
        # this if statement insures that TypeFacade is a singleton
        # this prevents reloading of the domain and other wasteful operations
        if self.state is None:
            self.type = TypeMain()
            self.type_logs = TypeLogs()
            
            self.memory_mapping = MemoryMapping()
            
            super().__init__(CONFIGURATION_PATH_TEMPLATE, None, ACTION_MAPPING_PATH, self.type_logs )
            TypeFacade.state = self.__dict__
        else:
            self.__dict__ = TypeFacade.state
    
    def initialize(self, request, response):
        self.type.initialize(request, response)
        self.memory_mapping.initialize(request, response)
        super().initialize(request, response)
    
    def get_logs(self):
        self.type_logs.get_logs(**self.request.get_values())
        
    def memory_map_machine_readable_to_human_readable(self):
        self.memory_mapping.get_human_readable_type(**self.request.get_values())
        
    def memory_map_human_readable_to_machine_readable(self):
        self.memory_mapping.get_machine_readable_type(**self.request.get_values())
        
    def memory_register_human_to_machine_mapping(self):
        self.memory_mapping.register_human_to_machine_mapping(**self.request.get_values())
    
    def memory_register_machine_to_human_mapping(self):
        self.memory_mapping.register_machine_to_human_mapping(**self.request.get_values())