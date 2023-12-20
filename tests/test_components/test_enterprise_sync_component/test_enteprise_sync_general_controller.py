from unittest.mock import patch

from FreeTAKServer.core.enterprise_sync.enterprise_sync_facade import EnterpriseSync
from tests.test_components.misc import ComponentTest
from tests.test_components.test_cot_manager_component.test_cot_manager_schemas import (
    TEST_CONNECTION_SCHEMA, TEST_CREATE_REPEATED_MESSAGE_SCHEMA,
    TEST_DELETE_NON_EXISTENT_REPEATED_MESSAGE_SCHEMA,
    TEST_DELETE_REPEATED_MESSAGE_SCHEMA, TEST_GET_REPEATED_MESSAGES_SCHEMA
)

def test_save_enterprise_sync_data():
    """ test the save enterprise sync data method works as follows:
    1. call save enterprise sync data from the enterprise sync facade
    2. call save enterprise sync data from the enterprise_sync_general_controller
    3. call convert_newlines from the enterprise_sync_format_sync_controller
    4. call save_file from the enterprise_sync_filesystem_controler
    """