
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.util.time_utils import get_current_datetime


def create_enterprise_sync_metadata():
    enterprise_sync_metadata = EnterpriseSyncDataObject()

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