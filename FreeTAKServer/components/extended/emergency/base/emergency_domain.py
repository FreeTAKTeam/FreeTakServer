from FreeTAKServer.components.core.abstract_component.domain import Domain
from ..configuration.emergency_constants import CONFIGURATION_PATH_TEMPLATE
from .. import domain


class EmergencyDomain(Domain):
    def __init__(self, request, response, configuration, action_mapper):
        super().__init__(
            CONFIGURATION_PATH_TEMPLATE,
            domain,
            request=request,
            response=response,
            configuration=configuration,
            action_mapper=action_mapper,
        )
