from uuid import uuid4
from FreeTAKServer.components.core.domain.domain import Event

from ...domain import MissionInvitationList
from ...domain import permissions as ModelPermissions, permission as ModelPermission

from FreeTAKServer.components.core.domain.domain._role import role
from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_INVITATION_NOTIFICATION
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain.mission_list_cot_content import MissionListCoTContent
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.domain.domain import MissionInfo
from FreeTAKServer.components.extended.mission.persistence.mission_invitation import MissionInvitation
from FreeTAKServer.core.util.time_utils import get_dtg
from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()

class MissionInvitationNotificationBuilder(Builder):
    """Builds a mission list cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: Event = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission list change object"""
        self.request.set_value("object_class_name", "Event")
        
        configuration = config_loader.find_configuration(MISSION_INVITATION_NOTIFICATION)
        
        self.result = super()._create_model_object(configuration, extended_domain={"role": role, "permissions": ModelPermissions, "permission": ModelPermission})
    
    def add_object_data(self, mapped_object: MissionInvitation):
        """adds the data from the mapped object to the result object"""

        self.result.uid = str(uuid4())
        self.result.type = "t-x-m-i"
        self.result.version = "2.0"
        self.result.how = "h-g-i-g-o"
        
        self.result.detail.mission.type = "INVITE"
        self.result.detail.mission.tool = "public"
        self.result.detail.mission.name = mapped_object.subscription.mission.name
        self.result.detail.mission.authorUid = mapped_object.author_uid
        self.result.detail.mission.token = mapped_object.subscription.token
        self.result.detail.mission.role.type = mapped_object.subscription.role.role_type

    def get_result(self):
        return self.result