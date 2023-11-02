from typing import TYPE_CHECKING
from uuid import uuid4

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_EXTERNAL_DATA_NOTIFICATION
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import detail, notes, externalData, tool, urlData, urlView
from FreeTAKServer.components.extended.mission.persistence.external_data import ExternalData
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.domain.domain import MissionChangeRecord
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.util.time_utils import get_current_dtg

if TYPE_CHECKING:
    from FreeTAKServer.components.core.domain.domain import Event


class MissionExternalDataNotificationBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionChangeRecord = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "Event")

        configuration = config_loader.find_configuration(MISSION_EXTERNAL_DATA_NOTIFICATION)

        self.result: Event = super()._create_model_object(configuration, extended_domain={"notes": notes, "externalData": externalData, "tool": tool, "urlData": urlData, "urlView": urlView})

    def add_object_data(self, mapped_object: ExternalData):
        """adds the data from the mapped object to the mission """
        self.result.uid = uuid4()
        self.result.type = "t-x-m-c-e"
        self.result.how = "h-g-i-g-o"

        self.result.point.lat = 0
        self.result.point.lon = 0
        self.result.point.ce = 9999999
        self.result.point.le = 9999999
        self.result.point.hae = 0

        self.result.detail.mission.authorUid = mapped_object.creator_uid
        self.result.detail.mission.name = mapped_object.mission_uid
        self.result.detail.mission.type = "CHANGE"
        self.result.detail.mission.tool = "public"
        
        self.result.detail.mission.MissionChanges.MissionChange[0].creatorUid.text = mapped_object.creator_uid
        self.result.detail.mission.MissionChanges.MissionChange[0].contentUid.text = mapped_object.id
        self.result.detail.mission.MissionChanges.MissionChange[0].isFederatedChange.text = "false"
        self.result.detail.mission.MissionChanges.MissionChange[0].missionName.text = mapped_object.mission.name
        self.result.detail.mission.MissionChanges.MissionChange[0].timestamp.text = get_current_dtg()
        self.result.detail.mission.MissionChanges.MissionChange[0].type.text = "ADD_CONTENT"

        self.result.detail.mission.MissionChanges.MissionChange[0].externalData.name.text = mapped_object.name
        self.result.detail.mission.MissionChanges.MissionChange[0].externalData.tool.text = mapped_object.tool
        self.result.detail.mission.MissionChanges.MissionChange[0].externalData.notes.text = mapped_object.notes
        self.result.detail.mission.MissionChanges.MissionChange[0].externalData.urlData.text = mapped_object.urlData
        self.result.detail.mission.MissionChanges.MissionChange[0].externalData.urlView.text = mapped_object.urlView
        self.result.detail.mission.MissionChanges.MissionChange[0].externalData.uid.text = mapped_object.id

    def get_result(self):
        """gets the result of the builder"""
        return self.result