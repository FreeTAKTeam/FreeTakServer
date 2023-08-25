from unittest.mock import patch
import FreeTAKServer

from FreeTAKServer.components.extended.mission.mission_facade import Mission
from FreeTAKServer.components.extended.mission.persistence.log import Log
from FreeTAKServer.components.extended.mission.persistence.mission import Mission as MissionDBObj
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent
from FreeTAKServer.components.extended.mission.persistence.mission_log import MissionLog
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject
from FreeTAKServer.core.util.time_utils import get_current_datetime

from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.mission_model_test_utils import add_test_mission_content, create_cot, create_enterprise_sync_metadata, create_test_mission, create_log, add_log_to_mission
from tests.test_components.test_mission_component.test_mission_notification_controller_schemas import TEST_COT_CREATED_NOTIFICATION_SCHEMA, TEST_NEW_MISSION_SCHEMA
from digitalpy.core.main.object_factory import ObjectFactory

@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission')
def test_mission_created_notification(get_mission_mock):
    """test the mission_created_notification action in the mission_notification_controller
    passing the Mission input object with example values and mocking the execute_sub_action method
    """
    setup = ComponentTest(TEST_NEW_MISSION_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    mission = MissionDBObj()

    mission.name = "test_mission"

    mission.tool = "test_tool"
    
    mission.creatorUid = "test_creator_uid"

    setup.request.set_value('mission_id', "test_mission")
    
    get_mission_mock.return_value = mission

    facade.mission_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']
    
@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_log')
def test_log_created_notification(get_log_mock):
    """test the mission_created_notification action in the mission_notification_controller
    passing the Mission input object with example values and mocking the execute_sub_action method
    """
    setup = ComponentTest(TEST_NEW_MISSION_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    mission = create_test_mission()

    log = create_log()

    add_log_to_mission(mission, log)

    get_log_mock.return_value = log

    setup.request.set_value('log_id', "test_log")
    
    facade.mission_log_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']

@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission_change')
def test_mission_content_created_notification(get_mission_change_mock):
    """test the mission_created_notification action in the mission_notification_controller
    passing the Mission input object with example values and mocking the execute_sub_action method
    """
    setup = ComponentTest(TEST_NEW_MISSION_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    mission = create_test_mission()

    add_test_mission_content(mission)
    
    enterprise_sync_data = create_enterprise_sync_metadata()

    setup.request.set_value('content_id', "test_mission")
    
    get_mission_change_mock.return_value = mission.contents[0].change[0]

    def simple_function_call_side_effect(self, *args, **kwargs):
        self.response.set_value('objectmetadata', enterprise_sync_data)

    with patch.object(FreeTAKServer.core.enterprise_sync.controllers.enterprise_sync_general_controller.EnterpriseSyncGeneralController, 'get_enterprise_sync_metadata', side_effect=simple_function_call_side_effect, autospec=True) as get_enterprise_sync_metadata_mock:
        get_enterprise_sync_metadata_mock.return_value = None

        facade.mission_content_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']

@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission_cot')
def test_cot_created_notification(get_mission_cot_mock):
    """test the send_cot_created_notification action in the mission_notification_controller
    """
    setup = ComponentTest(TEST_COT_CREATED_NOTIFICATION_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    mission = create_test_mission()

    cot = create_cot()

    mission.cots.append(cot)
    
    get_mission_cot_mock.return_value = cot

    setup.request.set_value('mission_cot_id', "test")

    facade.send_cot_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']
