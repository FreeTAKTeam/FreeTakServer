from .mapping_interface import MappingInterface
from digitalpy.routing.controller import Controller


class MemoryMapping(MappingInterface, Controller):

    machine_to_human_mapping = {}
    human_to_machine_mapping = {}

    def __init__(self, request, response, action_mapper, configuration):
        super().__init__(
            request=request,
            response=response,
            action_mapper=action_mapper,
            configuration=configuration,
        )
        self.machine_to_human_mapping = MemoryMapping.machine_to_human_mapping
        self.human_to_machine_mapping = MemoryMapping.human_to_machine_mapping

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())

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
