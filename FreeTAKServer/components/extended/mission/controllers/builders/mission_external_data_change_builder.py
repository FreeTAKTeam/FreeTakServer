from typing import TYPE_CHECKING

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_CHANGE_RECORD
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import detail, externalData
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.domain.domain import MissionChangeRecord
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.util.time_utils import get_dtg

if TYPE_CHECKING:
    from FreeTAKServer.components.core.domain.domain import Event


class MissionExternalDataChangeBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionChangeRecord = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "MissionChangeRecord")

        configuration = config_loader.find_configuration(MISSION_CHANGE_RECORD)

        self.result = super()._create_model_object(configuration, extended_domain={"detail": detail, "MissionExternalData": externalData})

    def add_object_data(self, mapped_object: MissionChange):
        """adds the data from the mapped object to the mission """
        self.result.type = mapped_object.type
        self.result.creatorUid = mapped_object.creator_uid
        self.result.missionName = mapped_object.mission_uid
        self.result.serverTime = get_dtg(mapped_object.server_time)
        self.result.timestamp = get_dtg(mapped_object.timestamp)
        self.result.contentUid = mapped_object.content_uid
        self.result.contentResource = None

        if mapped_object.external_data_uid != None:
            self.result.externalData.name = mapped_object.external_data.name
            self.result.externalData.tool = mapped_object.external_data.tool
            self.result.externalData.urlData = mapped_object.external_data.urlData
            self.result.externalData.urlView = mapped_object.external_data.urlView
            self.result.externalData.notes = mapped_object.external_data.notes
            self.result.externalData.uid = mapped_object.external_data.uid

    def get_result(self):
        """gets the result of the builder"""
        return self.result