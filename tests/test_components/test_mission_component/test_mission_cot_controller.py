from unittest.mock import patch, MagicMock
from FreeTAKServer.components.extended.mission.mission_facade import Mission
from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.mission_model_test_utils import create_mission_cot
from tests.test_components.test_mission_component.test_mission_cot_controller_schemas import TEST_GET_MISSION_COTS_SCHEMA, TEST_MISSION_COT_ADDED_SCHEMA
from digitalpy.core.main.object_factory import ObjectFactory
from lxml import etree

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

@patch('FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission_cots')
@patch('FreeTAKServer.components.extended.mission.controllers.mission_domain_controller.MissionDomainController.create_events')
def test_get_mission_cots(create_events_mock, get_mission_cots_mock):
    """get mission cots works as follows
    1. call get_mission_cots from the mission facade
    2. call get_mission_cots from the mission_cot_controller
    3. call get_mission_cots from the mission_persistence_controller [Mocked]
    4. call get_cot from the cot_management_facade (through action mapper)
    5-9. serialize each CoT to XML and build the events container
    """
    setup = ComponentTest(TEST_GET_MISSION_COTS_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    # real events container so events.xml.append() works
    events_obj = MagicMock()
    events_obj.xml = etree.Element("events")
    create_events_mock.return_value = events_obj

    cot_a = create_mission_cot()
    cot_a.uid = "test_uid_a"
    cot_a.xml_content = "<event>a data</event>"
    cot_b = create_mission_cot()
    cot_b.uid = "test_uid_b"
    cot_b.xml_content = "<event>b data</event>"
    get_mission_cots_mock.return_value = [cot_a, cot_b]

    # map uid -> xml bytes for the per-cot NodeToXML calls
    cot_xml_map = {
        "test_uid_a": b"<event>a data</event>",
        "test_uid_b": b"<event>b data</event>",
    }
    node_to_xml_call_count = 0

    def sub_action_side_effect(action_name):
        nonlocal node_to_xml_call_count
        response = MagicMock()
        if action_name == "GetCoT":
            response.get_value.return_value = MagicMock()
        elif action_name == "NodeToXML":
            node_to_xml_call_count += 1
            if node_to_xml_call_count <= len(cot_xml_map):
                # per-cot call: look up by cot_id on the request
                cot_id = facade.cot_controller.request.get_value("cot_id")
                response.get_value.return_value = cot_xml_map[cot_id]
            else:
                # final call: serialise the fully-built events element
                response.get_value.return_value = etree.tostring(events_obj.xml)
        return response

    with patch.object(facade.cot_controller, 'execute_sub_action', side_effect=sub_action_side_effect):
        facade.get_mission_cots(**setup.request.get_values())

    assert setup.response.get_value("cots") == b"<events><event>a data</event><event>b data</event></events>"