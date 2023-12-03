from unittest.mock import patch
from FreeTAKServer.components.extended.mission.mission_facade import Mission
from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.mission_model_test_utils import create_cot
from tests.test_components.test_mission_component.test_mission_cot_controller_schemas import TEST_GET_MISSION_COTS_SCHEMA, TEST_MISSION_COT_ADDED_SCHEMA
from digitalpy.core.main.object_factory import ObjectFactory

@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.create_mission_cot')
@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.create_mission_change')
def test_mission_cot_added(create_mission_change, create_mission_cot):
    setup = ComponentTest(TEST_MISSION_COT_ADDED_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    facade.create_mission_cot(**setup.request.get_values())

    assert create_mission_change.call_count == 1
    assert create_mission_cot.call_count == 1
    assert create_mission_cot.call_args[1]['mission_id'] == setup.request.get_value('mission_ids')[0]
    assert create_mission_cot.call_args[1]['type'] == setup.request.get_value('cot_type')
    assert create_mission_cot.call_args[1]['callsign'] == setup.request.get_value('callsign')
    assert create_mission_cot.call_args[1]['uid'] == setup.request.get_value('uid')

@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission_cots')
def test_get_mission_cots(get_mission_cots_mock):
    """returns all cots for a mission"""
    setup = ComponentTest(TEST_GET_MISSION_COTS_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    cot_a = create_cot()
    cot_a.uid = "test_uid_a"
    cot_a.xml_content = "<event>a data</event>"
    cot_b = create_cot()
    cot_b.uid = "test_uid_b"
    cot_b.xml_content = "<event>b data</event>"
    get_mission_cots_mock.return_value = [cot_a, cot_b]

    facade.get_mission_cots(**setup.request.get_values())

    assert setup.response.get_value("cots") == b"<events><event>a data</event><event>b data</event></events>"