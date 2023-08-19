from unittest.mock import patch

from FreeTAKServer.components.extended.mission.mission_facade import Mission
from FreeTAKServer.components.extended.mission.persistence.mission import Mission as MissionDBObj
from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.test_mission_notification_controller_schemas import TEST_NEW_MISSION_SCHEMA
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