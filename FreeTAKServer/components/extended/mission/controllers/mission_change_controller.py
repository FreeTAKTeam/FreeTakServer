from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.util.serialization_utils import serialize_to_json
from FreeTAKServer.core.util.time_utils import get_dtg

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from digitalpy.core.parsing.load_configuration import LoadConfiguration

config = MainConfig.instance()

class MissionChangeController(Controller):
    """manage mission change requests"""

    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.domain_controller = MissionDomainController(request, response, sync_action_mapper, configuration)
        self.persistence_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)

    def initialize(self, request, response):
        """initialize the controller"""
        super().initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.persistence_controller.initialize(request, response)

    def execute(self, method=None):
        getattr(self, method)(**self.request.get_values())
        return self.response
    
    def create_mission_record(self, mission_uid, creator_uid):
        self.persistence_controller.create_mission_change(
                type = "CREATE_MISSION",
                mission_uid=mission_uid,
                creator_uid=creator_uid,
                content_uid=None,
                cot_detail_uid=None,
                content_resource_uid=None
            )

    def create_mission_content_upload_record(self, mission_content_uid, creator_uid, content_uid):
        self.persistence_controller.create_mission_change(
                type = "ADD_CONTENT",
                mission_uid=mission_content_uid,
                creator_uid=creator_uid,
                content_uid=None,
                cot_detail_uid=None,
                content_resource_uid=content_uid
            )
        
    def create_mission_cot_record(self, mission_cot_uid, creator_uid, cot_uid):
        self.persistence_controller.create_mission_change(
                type = "ADD_CONTENT",
                mission_uid=mission_cot_uid,
                creator_uid=creator_uid,
                content_uid=None,
                cot_detail_uid=cot_uid,

                content_resource_uid=None
            )

    def get_mission_changes(self, mission_id, config_loader, *args, **kwargs):
        change_collection = self.domain_controller.create_mission_collection(config_loader)
        change_collection.type = "MissionChange"
        change_collection.version = "3"
        change_collection.nodeId = config.nodeID

        mission = self.persistence_controller.get_mission(mission_id)
        if mission == None:
            self.response.set_value("mission_changes", None)
            return None
        else:
            mission_changes = mission.changes
        for change in mission_changes:
            change_record = self.domain_controller.create_mission_change_record(config_loader)
            change_record.type = change.type
            change_record.creatorUid = change.creator_uid
            change_record.missionName = change.mission_uid
            change_record.serverTime = get_dtg(change.server_time)
            change_record.timestamp = get_dtg(change.timestamp)
            change_record.contentUid = change.content_uid

            if change.content_resource_uid != None:
                mission_content = self.domain_controller.create_mission_content_data(config_loader)
                self.request.set_value("objectuid", change.content_resource_uid)
                self.request.set_value("objecthash", change.content_resource_uid)
                enterprise_sync_db: 'EnterpriseSyncDataObject' = self.execute_sub_action("GetEnterpriseSyncMetaData").get_value("objectmetadata")
                
                change_record.contentResource = self.domain_controller.complete_mission_content_data(mission_content, enterprise_sync_db)

            elif change.cot_detail_uid != None:
                mission_cot = self.domain_controller.create_mission_cot_change(config_loader)
                self.request.set_value("cot_uid", change.cot_detail_uid)
                mission_cot_db = change.cot_detail
                change_record.detail = self.domain_controller.complete_mission_cot_change(mission_cot_db, mission_cot)
                
            change_collection.data = change_record
        
        serialized_change_collections = serialize_to_json(change_collection, self.request, self.execute_sub_action)

        self.response.set_value("mission_changes", serialized_change_collections)
        return serialized_change_collections
