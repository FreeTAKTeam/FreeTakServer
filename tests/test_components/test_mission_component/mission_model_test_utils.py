from unittest.mock import MagicMock
from FreeTAKServer.components.extended.mission.persistence.log import Log
from FreeTAKServer.components.extended.mission.persistence.mission import Mission as MissionDBObj
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent
from FreeTAKServer.components.extended.mission.persistence.mission_cot import MissionCoT
from FreeTAKServer.components.extended.mission.persistence.mission_log import MissionLog
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.util.time_utils import get_current_datetime

def create_test_mission():
    mission = MagicMock(MissionDBObj)

    mission.name = "test_mission"

    mission.PrimaryKey = "test_mission"

    mission.tool = "test_tool"
    
    mission.creatorUid = "test_creator_uid"

    mission.createTime = get_current_datetime()

    mission.cots = []

    return mission

def create_enterprise_sync_metadata():
    enterprise_sync_metadata = MagicMock(EnterpriseSyncDataObject)

    enterprise_sync_metadata.start_time = get_current_datetime()

    enterprise_sync_metadata.PrimaryKey = "test_mission_content_id"

    enterprise_sync_metadata.id = 1

    enterprise_sync_metadata.file_type = "Test"

    enterprise_sync_metadata.hash = "abc123"

    enterprise_sync_metadata.length = 100

    enterprise_sync_metadata.mime_type = "application/xml"

    enterprise_sync_metadata.submitter = "test_submitter"

    enterprise_sync_metadata.tool = "public"

    enterprise_sync_metadata.creator_uid = "test_creator_uid"

    enterprise_sync_metadata.file_name = "test_file_name"

    enterprise_sync_metadata.private = 0

    return enterprise_sync_metadata

def add_test_mission_content(mission: MissionDBObj):
    mission_content = MagicMock(MissionContent)

    mission_content.PrimaryKey = "test_mission_content_id"

    mission_content.mission = mission

    mission.contents.append(mission_content)

    mission_change = MissionChange()

    mission_content.change.append(mission_change)

    mission.changes.append(mission_change)

    mission_change.mission = mission

    mission_change.content_resource = mission_content

    mission_change.content_resource_uid = "test_mission_content_id"

    mission_change.content_uid = mission_content.PrimaryKey

    mission_change.creator_uid = "test_creator_uid"

    mission_change.type = "ADD_CONTENT"

    mission_change.server_time = get_current_datetime()

    mission_change.timestamp = get_current_datetime()

def create_log():
    log = Log(id = "test_mission_log_id")

    log.entryUid = "test_mission_log_entry_uid"

    log.creatorUid = "test_creator_uid"

    log.content = "test_content"

    log.servertime = get_current_datetime()

    log.dtg = get_current_datetime()

    log.created = get_current_datetime()

    log.contentHashes = "test_content_hashes"

    log.keywords = "test_keywords"

    return log

def add_log_to_mission(mission: MissionDBObj, log: Log):
    mission_log = MagicMock(MissionLog)

    mission_log.mission = mission

    mission_log.log = log

    mission.logs.append(mission_log)

    log.missions.append(mission_log)

def create_mission_cot():
    cot = MagicMock(MissionCoT)

    cot.callsign = "test_callsign"

    cot.iconset_path = "test_iconset_path"

    cot.lat = 1.0

    cot.lon = 1.0

    cot.uid = "test_cot_uid"

    cot.type = "test_cot_type"

    cot.xml_content = "<event></event>"

    cot.create_time = get_current_datetime()

    return cot

def create_event_db():
    