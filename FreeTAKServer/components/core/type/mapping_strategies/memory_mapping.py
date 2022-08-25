from .mapping_interface import MappingInterface
from digitalpy.routing.controller import Controller


class MemoryMapping(MappingInterface, Controller):

    machine_to_human_mapping = {}
    human_to_machine_mapping = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.machine_to_human_mapping = MemoryMapping.machine_to_human_mapping
        self.human_to_machine_mapping = MemoryMapping.human_to_machine_mapping

    def get_machine_readable_type(self, human_readable_type, default=None, **kwargs):
        self.response.set_value(
            "machine_readable_type",
            self.human_to_machine_mapping.get(human_readable_type, default),
        )

    def get_human_readable_type(self, machine_readable_type, default=None, **kwargs):
        self.response.set_value(
            "human_readable_type",
            self.machine_to_human_mapping.get(machine_readable_type, default),
        )

    def register_machine_to_human_mapping(
        self, machine_to_human_mapping: dict, **kwargs
    ):
        self.machine_to_human_mapping.update(machine_to_human_mapping)

    def register_human_to_machine_mapping(
        self, human_to_machine_mapping: dict, **kwargs
    ):
        self.human_to_machine_mapping.update(human_to_machine_mapping)
