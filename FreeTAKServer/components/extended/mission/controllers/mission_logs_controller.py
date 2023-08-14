import json
from typing import List, Dict
from uuid import uuid4
from FreeTAKServer.components.extended.excheck.domain.mission_info import MissionInfo
from FreeTAKServer.components.extended.mission.controllers.mission_domain_controller import MissionDomainController
from FreeTAKServer.components.extended.mission.controllers.mission_general_controller import MissionGeneralController
from FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller import MissionPersistenceController
from FreeTAKServer.components.core.domain.domain import MissionLog
from FreeTAKServer.components.extended.mission.persistence.log import Log
from FreeTAKServer.components.extended.mission.persistence.mission_log import MissionLog as DBMissionLog
from FreeTAKServer.core.domain.node import Node
from FreeTAKServer.core.util.serialization_utils import serialize_to_json
from FreeTAKServer.core.util.time_utils import get_current_datetime, get_datetime_from_dtg, get_dtg, get_past_datetime
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.request import Request
from digitalpy.core.zmanager.response import Response
from digitalpy.core.zmanager.action_mapper import ActionMapper
from digitalpy.core.digipy_configuration.configuration import Configuration
from datetime import datetime as dt

from FreeTAKServer.core.configuration.MainConfig import MainConfig

DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"

from ..configuration.mission_constants import (
    BASE_OBJECT_NAME,
    MISSION_CONTENT,
    MISSION_ITEM,
    MISSION_SUBSCRIPTION_DATA,
    MISSION_NOTIFICATION
)

config = MainConfig.instance()

class MissionLogsController(Controller):
    
    def __init__(
        self,
        request: Request,
        response: Response,
        sync_action_mapper: ActionMapper,
        configuration: Configuration,
        ):
        super().__init__(request, response, sync_action_mapper, configuration)
        self.persistency_controller = MissionPersistenceController(request, response, sync_action_mapper, configuration)
        self.domain_controller = MissionDomainController(request, response, sync_action_mapper, configuration)
        self.general_controller = MissionGeneralController(request, response, sync_action_mapper, configuration)
        
    def initialize(self, request: Request, response: Response):
        super().initialize(request, response)
        self.persistency_controller.initialize(request, response)
        self.domain_controller.initialize(request, response)
        self.general_controller.initialize(request, response)
        
    def add_mission_log(self, mission_log_data: Dict, config_loader, *args, **kwargs):
        log_db_obj = self.persistency_controller.create_log(
            id = str(uuid4()),
            uid = mission_log_data["entryUid"], 
            mission_ids=mission_log_data["missionNames"], 
            dtg=get_datetime_from_dtg(mission_log_data["dtg"]), 
            creatorUid=mission_log_data["creatorUid"], 
            servertime=get_current_datetime(), 
            created=get_current_datetime(), 
            content=json.dumps(mission_log_data.get("contentHashes", [])), 
            keywords=json.dumps(mission_log_data["keywords"]))
        log_domain_obj = self.domain_controller.create_log(config_loader)
        completed_obj = self.complete_mission_log_object(log_domain_obj, log_db_obj)
        serialized_message = serialize_to_json(completed_obj, self.request, self.execute_sub_action)
        
        self.response.set_value("log", serialized_message)
        return serialized_message
        
    def get_mission_logs(self, mission_id, seconds_ago, start, end, config_loader, *args, **kwargs):
        """Get mission logs for a mission"""
        start_time = None
        end_time = None
        
        if seconds_ago is not None:
            start_time = get_past_datetime(int(seconds_ago))
            end_time = get_current_datetime()
            
        elif start is not None and end is not None:
            start_time = get_datetime_from_dtg(start)
            end_time = get_datetime_from_dtg(end)
        
        if start_time is not None and end_time is not None: 
            logs = self.persistency_controller.get_mission_logs_by_time(mission_id, start_time, end_time)
        else: 
            logs = self.persistency_controller.get_mission_logs(mission_id)
        log_collection_obj = self.domain_controller.create_log_collection(config_loader)
        logs = [mission_log.log for mission_log in logs]
        completed_collection = self.complete_log_collection_object(log_collection_obj, logs, config_loader)
        
        serialized_collection = serialize_to_json(completed_collection, self.request, self.execute_sub_action)
        
        self.response.set_value("logs", serialized_collection)
        return serialized_collection
        
    def update_mission_log(self, mission_log_data: Dict, config_loader, *args, **kwargs):
        if mission_log_data.get("dtg") is not None:
            dtg = get_datetime_from_dtg(mission_log_data["dtg"])
        else:
            dtg = None
            
        log_db_obj = self.persistency_controller.update_log(
                id=mission_log_data.get("id"),
                entryUid=mission_log_data.get("entryUid"), 
                mission_ids=mission_log_data.get("missionNames"), 
                dtg=dtg, 
                creatorUid=mission_log_data.get("creatorUid"), 
                content=json.dumps(mission_log_data.get("contentHashes")), 
                keywords=json.dumps(mission_log_data.get("keywords")))
        log_domain_obj = self.domain_controller.create_log(config_loader)
        completed_obj = self.complete_mission_log_object(log_domain_obj, log_db_obj)
        serialized_message = serialize_to_json(completed_obj, self.request, self.execute_sub_action)
        
        self.response.set_value("log", serialized_message)
        return serialized_message
    
    def complete_mission_log_object(self, mission_log_domain_obj: MissionLog, log_db_obj: Log) -> MissionLog:
        """Completes the mission log object with the data from the database object"""
        mission_log_domain_obj.entryUid = log_db_obj.entryUid
        
        mission_log_domain_obj.dtg = get_dtg(log_db_obj.dtg)
        mission_log_domain_obj.creatorUid = log_db_obj.creatorUid
        mission_log_domain_obj.servertime = get_dtg(log_db_obj.servertime)
        mission_log_domain_obj.created = get_dtg(log_db_obj.created)
        mission_log_domain_obj.contentHashes = json.loads(log_db_obj.content)
        mission_log_domain_obj.keywords = json.loads(log_db_obj.keywords)
        mission_log_domain_obj.id = log_db_obj.id

        for mission_log in log_db_obj.missions:
            mission_log_domain_obj.missionNames.append(mission_log.mission_uid)
        
        return mission_log_domain_obj
        
    def complete_log_collection_object(self, log_collection_domain_obj: MissionInfo, mission_log_db_objs: List[Log], config_loader, *args, **kwargs) -> MissionInfo:
        
        log_collection_domain_obj.version = "3"
        
        log_collection_domain_obj.type = "com.bbn.marti.sync.model.LogEntry"
        
        log_collection_domain_obj.nodeId = config.nodeID
        
        for mission_log_db in mission_log_db_objs:
            
            mission_log_domain_obj = self.domain_controller.create_log(config_loader)
            
            completed_obj = self.complete_mission_log_object(mission_log_domain_obj, mission_log_db)
            
            log_collection_domain_obj.data = completed_obj
        
        return log_collection_domain_obj
    
    def get_all_logs(self, config_loader, *args, **kwargs):
        logs = self.persistency_controller.get_all_logs()
        log_collection_obj = self.domain_controller.create_log_collection(config_loader)
        completed_collection = self.complete_log_collection_object(log_collection_obj, logs, config_loader)
        
        serialized_collection = serialize_to_json(completed_collection, self.request, self.execute_sub_action)
        
        self.response.set_value("logs", serialized_collection)
        return serialized_collection
        
    def get_log(self, log_id, config_loader, *args, **kwargs):
        logs = [self.persistency_controller.get_log(log_id)]
        log_collection_obj = self.domain_controller.create_log_collection(config_loader)
        completed_collection = self.complete_log_collection_object(log_collection_obj, logs, config_loader)
        
        serialized_collection = serialize_to_json(completed_collection, self.request, self.execute_sub_action)
        
        self.response.set_value("log", serialized_collection)
        return serialized_collection
        
    def delete_mission_log(self, log_id: str, config_loader, *args, **kwargs):
        self.persistency_controller.delete_mission_log(log_id)
        
    def get_time(self):
        now = dt.utcnow()
        return now.strftime(DATETIME_FMT)