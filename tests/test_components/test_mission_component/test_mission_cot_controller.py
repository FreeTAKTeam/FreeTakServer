from unittest.mock import patch
from FreeTAKServer.components.extended.mission.mission_facade import Mission
from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.mission_model_test_utils import create_mission_cot
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
    assert create_mission_cot.call_args[1]['uid'] == setup.request.get_value('uid')

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_persistence_controller.CoTManagementPersistenceController.get_cot')
@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission_cots')
def test_get_mission_cots(get_mission_cots_mock, get_cots_mock):
    """get mission cots works as follows
    1. call get_mission_cots from the mission facade
    2. call get_mission_cots from the mission_cot_controller [Mocked]
    3. call get_mission_cots from the mission_persistence_controller [Mocked]
        - this should return a list of MissionCoT instances
    4. call get_cot from the cot_management_facade (through action mapper) 
    5. call MissionCoT from the cot_management_data_controller
    6. call get_cot from the cot_management_persistence_controller
        - this should return a DBEvent instance
    7. call create_standard_xml from the cot_management_domain_controller
        - this should return an Event instance
    8. call complete_standard_xml from the cot_management_domain_controller
        - this should return an Event instance with the correct values
    9. call convert_node_to_xml from the xml_serialization_controller
    """
    setup = ComponentTest(TEST_GET_MISSION_COTS_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    cot_a = create_mission_cot()
    cot_a.uid = "test_uid_a"
    cot_a.xml_content = "<event>a data</event>"
    cot_b = create_mission_cot()
    cot_b.uid = "test_uid_b"
    cot_b.xml_content = "<event>b data</event>"
    get_mission_cots_mock.return_value = [cot_a, cot_b]

    facade.get_mission_cots(**setup.request.get_values())

    assert setup.response.get_value("cots") == b"<events><event>a data</event><event>b data</event></events>"