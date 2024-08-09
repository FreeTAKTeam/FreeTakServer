from FreeTAKServer.components.core.fts_domain.domain import event
from ...domain import permission as ModelPermission

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_PERMISSION
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import details, location
from FreeTAKServer.components.extended.mission.domain import permission as MissionPermission
from FreeTAKServer.components.core.fts_domain.domain import role
from FreeTAKServer.components.extended.mission.persistence.permission import Permission
from FreeTAKServer.components.extended.mission.persistence.role import Role
from FreeTAKServer.core.util.time_utils import get_dtg

class MissionPermissionBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionPermission = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "MissionPermission")

        configuration = config_loader.find_configuration(MISSION_PERMISSION)

        self.result = super()._create_model_object(configuration, extended_domain={"MissionPermission": ModelPermission})
    
    def add_object_data(self, mapped_object: Permission):
        """adds the data from the mapped object to the result object"""
        self.result.type = mapped_object.permission_type

    def get_result(self):
        return self.result