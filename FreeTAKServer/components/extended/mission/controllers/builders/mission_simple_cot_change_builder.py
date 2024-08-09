from typing import TYPE_CHECKING

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_SIMPLE_COT_CHANGE
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import details
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.fts_domain.domain import MissionChangeRecord
from FreeTAKServer.core.util.time_utils import get_dtg

if TYPE_CHECKING:
    from FreeTAKServer.components.core.fts_domain.domain import event


class MissionSimpleCoTChangeBuilder(Builder):
    """Builds a simplified mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionChangeRecord = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a simplified mission change object"""
        self.request.set_value("object_class_name", "MissionChangeRecord")

        configuration = config_loader.find_configuration(MISSION_SIMPLE_COT_CHANGE)

        self.result = super()._create_model_object(configuration, extended_domain={"details": details})

    def add_object_data(self, mapped_object: MissionChange):
        """adds the data from the mapped object to the mission """
        self.request.set_value("cot_id", mapped_object.cot_detail_uid)
        cot: 'event' = self.execute_sub_action("GetCoT").get_value("cot")

        self.result.type = "ADD_CONTENT"
        self.result.contentUid = cot.uid
        self.result.missionName = mapped_object.mission_uid
        self.result.serverTime = cot.time
        self.result.timestamp = cot.time
        self.result.creatorUid = ""
        self.result.details.type = cot.type
        self.result.details.callsign = cot.detail.contact.callsign
        self.result.contentResource = None
        self.result.externalData = None

    def get_result(self):
        """gets the result of the builder"""
        return self.result