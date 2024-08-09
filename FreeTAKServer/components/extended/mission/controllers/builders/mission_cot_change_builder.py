from typing import TYPE_CHECKING

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_COT_CHANGE
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import detail
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.fts_domain.domain import MissionChangeRecord
from FreeTAKServer.core.util.time_utils import get_dtg

if TYPE_CHECKING:
    from FreeTAKServer.components.core.fts_domain.domain import event


class MissionCoTChangeBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionChangeRecord = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "detail")

        configuration = config_loader.find_configuration(MISSION_COT_CHANGE)

        self.result = super()._create_model_object(configuration, extended_domain={"detail": detail})

    def add_object_data(self, mapped_object: MissionCoT):
        """adds the data from the mapped object to the mission """
        self.request.set_value("cot_id", mapped_object.uid)
        cot: 'event' = self.execute_sub_action("GetCoT").get_value("cot")

        # set hardcoded values
        self.result.isFederatedChange = False
        self.result.creatorUid = ""

        # set values from mapped object at root
        self.result.type = "ADD_CONTENT"
        self.result.contentUid = mapped_object.uid
        self.result.missionName = mapped_object.mission.name
        self.result.timestamp = cot.time
        self.result.serverTime = cot.time
        
        r_details = self.result.details 

        r_details.callsign = cot.detail.contact.callsign
        
        r_details.iconsetPath = cot.detail.usericon.iconsetpath
        r_details.type = cot.type

        # set values from mapped object at location
        r_loc = r_details.location
        r_loc.lat = cot.point.lat
        r_loc.lon = cot.point.lon

    def get_result(self):
        """gets the result of the builder"""
        return self.result