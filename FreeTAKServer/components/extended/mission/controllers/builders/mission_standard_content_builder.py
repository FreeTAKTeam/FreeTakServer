from typing import TYPE_CHECKING

from FreeTAKServer.components.core.domain.domain import Event
from FreeTAKServer.components.extended.mission.configuration.mission_constants import MISSION_CONTENT
from FreeTAKServer.components.extended.mission.controllers.builders.builder import Builder
from FreeTAKServer.components.extended.mission.domain.mission_list_cot_content import MissionListCoTContent
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent as DBMissionContent
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.core.domain.domain import MissionContent, MissionContentData
from FreeTAKServer.core.util.time_utils import get_dtg

if TYPE_CHECKING:
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject

class MissionStandardContentBuilder(Builder):
    """Builds a standard mission content item"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: MissionContent = None

    def build_empty_object(self, config_loader, *args, **kwargs):
        """Builds a standard mission content object"""
        self.request.set_value("object_class_name", "MissionContent")

        configuration = config_loader.find_configuration(MISSION_CONTENT)

        self.result = super()._create_model_object(configuration, extended_domain={"MissionContent": MissionContent, "MissionContentData": MissionContentData})
    
    def add_object_data(self, mapped_object: 'MissionChange'):
        """adds the data from the mapped object to the result object"""
        self.request.set_value("objectuid", mapped_object.PrimaryKey)
        self.request.set_value("objecthash", mapped_object.PrimaryKey)

        enterprise_sync_db: 'EnterpriseSyncDataObject' = self.execute_sub_action("GetEnterpriseSyncMetaData").get_value("objectmetadata")

        # set values from mapped object at root
        self.result.creatorUid = enterprise_sync_db.creator_uid
        self.result.timestamp = enterprise_sync_db.start_time

        self.result.data.uid = enterprise_sync_db.PrimaryKey
        self.result.data.hash = enterprise_sync_db.hash
        self.result.data.name = enterprise_sync_db.file_name
        self.result.data.mimeType = enterprise_sync_db.mime_type
        self.result.data.size = enterprise_sync_db.length
        self.result.data.tool = enterprise_sync_db.tool
        self.result.data.submitter = enterprise_sync_db.submitter
        
        keywords = []
        for keyword in enterprise_sync_db.keywords:
            keywords.append(keyword.keyword)
            
        self.result.data.keywords = keywords
        self.result.data.expiration = enterprise_sync_db.expiration

    def get_result(self):
        return self.result