from FreeTAKServer.components.core.domain.domain import Event

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_INVITATION_LIST
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.controllers.mission_invitation_controller import MissionInvitationController
from FreeTAKServer.components.extended.mission.domain.mission_list_cot_content import MissionListCoTContent
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.domain.domain import MissionInfo
from FreeTAKServer.core.util.time_utils import get_dtg
from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()

class MissionInvitationListBuilder(Builder):
    """Builds a mission list cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission list change object"""
        self.request.set_value("object_class_name", "MissionInvitationList")
        
        configuration = config_loader.find_configuration(MISSION_INVITATION_LIST)
        
        self.result = super()._create_model_object(configuration)
    
    def add_object_data(self, mapped_object = None):
        """adds the data from the mapped object to the result object"""

        self.result.version = "3"
        self.result.type = "MissionInvitation"
        self.result.nodeId = config.nodeID

    def get_result(self):
        return self.result