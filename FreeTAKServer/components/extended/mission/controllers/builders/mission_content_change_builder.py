from typing import TYPE_CHECKING

from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_CHANGE_RECORD
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain import detail
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.domain.domain import MissionChangeRecord
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.util.time_utils import get_dtg

if TYPE_CHECKING:
    from FreeTAKServer.components.core.domain.domain import Event


class MissionContentChangeBuilder(Builder):
    """Builds a mission cot change object"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionChangeRecord = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a mission change object"""
        self.request.set_value("object_class_name", "MissionChangeRecord")

        configuration = config_loader.find_configuration(MISSION_CHANGE_RECORD)

        self.result = super()._create_model_object(configuration, extended_domain={"detail": detail})

    def add_object_data(self, mapped_object: MissionChange):
        """adds the data from the mapped object to the mission """
        self.result.type = mapped_object.type
        self.result.creatorUid = mapped_object.creator_uid
        self.result.missionName = mapped_object.mission_uid
        self.result.serverTime = get_dtg(mapped_object.server_time)
        self.result.timestamp = get_dtg(mapped_object.timestamp)
        self.result.contentUid = mapped_object.content_uid

        if mapped_object.content_resource_uid != None:
            self.request.set_value("objectuid", mapped_object.content_resource_uid)
            self.request.set_value("objecthash", mapped_object.content_resource_uid)
            enterprise_sync_db: 'EnterpriseSyncDataObject' = self.execute_sub_action("GetEnterpriseSyncMetaData").get_value("objectmetadata")
            
            self.result.contentResource.uid = enterprise_sync_db.PrimaryKey
            self.result.contentResource.hash = enterprise_sync_db.hash
            self.result.contentResource.name = enterprise_sync_db.file_name
            self.result.contentResource.mimeType = enterprise_sync_db.mime_type
            self.result.contentResource.size = enterprise_sync_db.length
            self.result.contentResource.tool = enterprise_sync_db.tool
            self.result.contentResource.submitter = enterprise_sync_db.submitter
            
            keywords = []
            for keyword in enterprise_sync_db.keywords:
                keywords.append(keyword.keyword)
                
            self.result.contentResource.keywords = keywords
            self.result.contentResource.expiration = enterprise_sync_db.expiration

        if mapped_object.cot_detail_uid != None:
            self.request.set_value("cot_id", mapped_object.cot_detail_uid)
            cot: 'Event' = self.execute_sub_action("GetCoT").get_value("cot")
            self.result.details.callsign = cot.detail.contact.callsign
            self.result.details.type = cot.type

    def get_result(self):
        """gets the result of the builder"""
        return self.result