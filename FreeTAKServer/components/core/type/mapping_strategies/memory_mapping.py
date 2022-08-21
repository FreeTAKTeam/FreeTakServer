from .mapping_interface import MappingInterface
from digitalpy.routing.controller import Controller

class MemoryMapping(MappingInterface, Controller):
    
    state = None
    
    def __init__(self):
        if self.state is None:
            self.machine_to_human_mapping = {}
            self.human_to_machine_mapping = {}
            MemoryMapping.state = self.__dict__
        else:
            self.__dict__ = MemoryMapping.state
    
    def get_machine_readable_type(self, human_readable_type, default=None, **kwargs):
        self.response.set_value('machine_readable_type', self.human_to_machine_mapping.get(human_readable_type, default))
    
    def get_human_readable_type(self, machine_readable_type, default=None, **kwargs):
        self.response.set_value('human_readable_type', self.machine_to_human_mapping.get(machine_readable_type, default))
    
    def register_machine_to_human_mapping(self, machine_to_human_mapping: dict, **kwargs):
        self.machine_to_human_mapping.update(machine_to_human_mapping)
        
    def register_human_to_machine_mapping(self, human_to_machine_mapping: dict, **kwargs):
        self.human_to_machine_mapping.update(human_to_machine_mapping)