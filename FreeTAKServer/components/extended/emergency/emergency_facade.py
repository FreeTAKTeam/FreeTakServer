from FreeTAKServer.components.core.abstract_component.facade import Facade
from FreeTAKServer.components.extended.emergency.emergency_constants import (
    CONFIGURATION_PATH_TEMPLATE,
    ACTION_MAPPING_PATH,
    TYPE_MAPPINGS,
    LOGGING_CONFIGURATION_PATH,
)
from . import domain
from .emergency_main import EmergencyMain


class EmergencyFacade(Facade):

    state = None

    def __init__(self, action_mapper, request, response, configuration):
        self.emergency = EmergencyMain(
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
        super().__init__(
            config_path_template=CONFIGURATION_PATH_TEMPLATE,
            domain=domain,
            action_mapping_path=ACTION_MAPPING_PATH,
            type_mapping=TYPE_MAPPINGS,
            logger_configuration=LOGGING_CONFIGURATION_PATH,
            controllers=[self.emergency],
            action_mapper=action_mapper,
            request=request,
            response=response,
            configuration=configuration,
        )
        EmergencyFacade.state = self.__dict__

    def emergency_alert(self, **kwargs):
        self.emergency.emergency_received(**self.request.get_values())

    def emergency_in_contact(self, **kwargs):
        self.emergency.emergency_received(**self.request.get_values())

    def emergency_geofence_breached(self, **kwargs):
        self.emergency.emergency_received(**self.request.get_values())

    def emergency_ring_the_bell(self, **kwargs):
        self.emergency.emergency_received(**self.request.get_values())

    def emergency_delete(self, **kwargs):
        self.emergency.emergency_delete(**self.request.get_values())

    def emergency_broadcast(self, **kwargs):
        self.emergency.emergency_broadcast(**self.request.get_values())

    def emergency_broadcast_all(self, **kwargs):
        self.emergency.emergency_broadcast_all(**self.request.get_values())
