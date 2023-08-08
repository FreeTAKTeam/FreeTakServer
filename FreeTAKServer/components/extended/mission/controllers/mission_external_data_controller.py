from typing import Dict
from FreeTAKServer.components.core.domain.domain import MissionExternalData
from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.core.domain.domain import MissionInfoSingle
from FreeTAKServer.components.extended.mission.persistence.external_data import ExternalData
from FreeTAKServer.core.util.serialization_utils import serialize_to_json
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration

from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()

class MissionExternalDataController(Controller):
    def __init__(self, request: Request, response: Response, sync_action_mapper: ActionMapper, configuration: Configuration):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistency_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)
        self.domain_controller = MissionDomainController(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)
        
    def add_mission_external_data(self, mission_id: str, mission_external_data: Dict, config_loader, *args, **kwargs):
        external_data_db = self.persistency_controller.add_external_data(
            mission_id=mission_id,
            name=mission_external_data["name"],
            tool=mission_external_data["tool"],
            urlData=mission_external_data["urlData"],
            notes=mission_external_data["notes"],
            uid=mission_external_data["uid"],
            urlView=mission_external_data["urlView"]
        )
        external_data_domain = self.domain_controller.create_external_data_collection(config_loader)
        completed_external_data_collection = self.complete_mission_external_data_collection(external_data_domain, external_data_db, config_loader)
        
        serialized_data = serialize_to_json(completed_external_data_collection, self.request, self.execute_sub_action)
        
        self.response.set_value("external_data", serialized_data)
        return completed_external_data_collection
        
    def complete_mission_external_data_collection(self, external_data_collection_domain_obj: MissionInfoSingle, mission_external_data: ExternalData, config_loader, *args, **kwargs):
        external_data_collection_domain_obj.version = "3"
        external_data_collection_domain_obj.type = "com.bbn.marti.sync.model.ExternalMissionData"
        external_data_collection_domain_obj.nodeId = config.nodeID
        external_data: MissionExternalData = external_data_collection_domain_obj.data
        
        if isinstance(external_data, MissionExternalData):
            self.complete_mission_external_data(external_data, mission_external_data)
        
        return external_data_collection_domain_obj
    
    def complete_mission_external_data(self, external_data_domain_obj: MissionExternalData, external_data_db: ExternalData) -> MissionExternalData:
        external_data_domain_obj.name = external_data_db.name
        external_data_domain_obj.notes = external_data_db.notes
        external_data_domain_obj.tool = external_data_db.tool
        external_data_domain_obj.uid = external_data_db.uid
        external_data_domain_obj.urlData = external_data_db.urlData
        external_data_domain_obj.urlView = external_data_db.urlView
        return external_data_domain_obj