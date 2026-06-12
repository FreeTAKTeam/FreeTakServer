from digitalpy.core.main.object_factory import ObjectFactory
from unittest.mock import patch, MagicMock

from FreeTAKServer.components.extended.mission.mission_facade import Mission
import FreeTAKServer

from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.mission_model_test_utils import add_test_mission_content, create_enterprise_sync_metadata, create_test_mission
from tests.test_components.test_mission_component.test_mission_general_schemas import TEST_MISSION_CONTENT_SCHEMA

@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.update_mission')
def test_add_contents_to_mission(update_mission_mock):
    """test the mission_created_notification action in the mission_notification_controller
    passing the Mission input object with example values and mocking the execute_sub_action method
    """
    setup = ComponentTest(TEST_MISSION_CONTENT_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    mission = create_test_mission()
    enterprise_sync_data = create_enterprise_sync_metadata()

    setup.request.set_value('mission_id', "test_mission")
    setup.request.set_value('hashes', [enterprise_sync_data.hash])

    def sub_action_side_effect(action_name):
        response = MagicMock()
        if action_name == "GetMultipleEnterpriseSyncMetaData":
            response.get_value.return_value = [enterprise_sync_data]
        elif action_name == "GetMultipleEnterpriseSyncData":
            response.get_value.return_value = [b'<xml>test</xml>']
        elif action_name == "serialize":
            response.get_value.return_value = ['{}']
        else:
            response.get_value.return_value = None
        return response

    mock_mission_obj = MagicMock()

    with patch.object(facade.general_controller, 'execute_sub_action', side_effect=sub_action_side_effect), \
            patch.object(facade.general_controller.mission_director, 'construct', return_value=mock_mission_obj), \
            patch.object(FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController, 'get_mission', return_value=mission) as get_mission_mock, \
            patch.object(FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController, 'create_mission_change') as create_mission_change, \
            patch.object(FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController, 'create_mission_content') as create_mission_content:

        facade.add_mission_contents(**setup.request.get_values())

    assert update_mission_mock.call_count == 1

    assert update_mission_mock.call_args[0][0] == mission.PrimaryKey
    assert update_mission_mock.call_args[1]['content'] == create_mission_content.return_value

    assert create_mission_change.call_args[1]['type'] == "ADD_CONTENT"
    assert create_mission_change.call_args[1]['mission_uid'] == mission.PrimaryKey
    assert create_mission_change.call_args[1]['content_resource_uid'] == enterprise_sync_data.hash