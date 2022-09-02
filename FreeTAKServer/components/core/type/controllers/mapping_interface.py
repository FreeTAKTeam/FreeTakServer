from abc import ABC

class MappingInterface(ABC):
    
    
    def get_machine_readable_type(self, human_readable_type, default=None):
        raise NotImplementedError
    
    def get_human_readable_type(self, machine_readable_type, default=None):
        raise NotImplementedError
    
    def register_machine_to_human_mapping(self, machine_to_human_mapping: dict):
        raise NotImplementedError
    
    def register_human_to_machine_mapping(self, human_to_machine_mapping: dict):
        raise NotImplementedError