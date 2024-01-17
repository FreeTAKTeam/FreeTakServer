from FreeTAKServer.components.core.fts_domain.domain import event

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_COT_CONTENT
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import details, location
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.fts_domain.domain import role
from FreeTAKServer.components.extended.mission.persistence.role import Role
from FreeTAKServer.core.util.time_utils import get_dtg

class MissionRoleBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: role = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "role")

        configuration = config_loader.find_configuration(MISSION_COT_CONTENT)

        self.result = super()._create_model_object(configuration, extended_domain={})
    
    def add_object_data(self, mapped_object: role):
        """adds the data from the mapped object to the result object"""
        self.result.permissions = [permission.permission.permission_type for permission in mapped_object.permissions]
        self.result.type = mapped_object.role_type

    def get_result(self):
        return self.result