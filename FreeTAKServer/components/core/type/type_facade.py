from FreeTAKServer.components.core.abstract_component.facade import Facade
from .type_constants import (
    ACTION_MAPPING_PATH,
    LOGGING_CONFIGURATION_PATH,
)
from .type_main import TypeMain
from .mapping_strategies import MemoryMapping


class TypeFacade(Facade):

    state = None

    def __init__(self, action_mapper, request, response, configuration):
        self.type = TypeMain(
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
        self.memory_mapping = MemoryMapping(
            action_mapper, request, response, configuration
        )

        super().__init__(
            config_path_template=None,
            action_mapping_path=ACTION_MAPPING_PATH,
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            controllers=[self.type, self.memory_mapping],
            domain=None,
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )

    def memory_map_machine_readable_to_human_readable(self, **kwargs):
        self.memory_mapping.get_human_readable_type(**self.request.get_values())

    def memory_map_human_readable_to_machine_readable(self, **kwargs):
        self.memory_mapping.get_machine_readable_type(**self.request.get_values())

    def memory_register_human_to_machine_mapping(self, **kwargs):
        self.memory_mapping.register_human_to_machine_mapping(
            **self.request.get_values()
        )

    def memory_register_machine_to_human_mapping(self, **kwargs):
        self.memory_mapping.register_machine_to_human_mapping(
            **self.request.get_values()
        )
