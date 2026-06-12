from unittest.mock import patch, MagicMock
import FreeTAKServer

from FreeTAKServer.components.extended.mission.mission_facade import Mission
from FreeTAKServer.components.extended.mission.persistence.log import Log
from FreeTAKServer.components.extended.mission.persistence.mission import Mission as MissionDBObj
from FreeTAKServer.components.extended.mission.persistence.mission_change import MissionChange
from FreeTAKServer.components.extended.mission.persistence.mission_content import MissionContent
from FreeTAKServer.components.extended.mission.persistence.mission_log import MissionLog
from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import \
    EnterpriseSyncDataObject
from FreeTAKServer.core.util.time_utils import get_current_datetime

from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.mission_model_test_utils import add_test_mission_content, \
    create_mission_cot, create_enterprise_sync_metadata, create_test_mission, create_log, add_log_to_mission
from tests.test_components.test_mission_component.test_mission_notification_controller_schemas import \
    TEST_COT_CREATED_NOTIFICATION_SCHEMA, TEST_NEW_MISSION_SCHEMA
from digitalpy.core.main.object_factory import ObjectFactory


def make_create_node_response():
    """Return a MagicMock that looks like a valid domain object for CreateNode responses."""
    node = MagicMock()
    return node


def make_domain_sub_action_side_effect(enterprise_sync_data=None):
    """Side effect for domain_controller.execute_sub_action: handles CreateNode and GetEnterpriseSyncMetaData calls."""

    def side_effect(action_name):
        response = MagicMock()
        if action_name == "CreateNode":
            response.get_value.return_value = make_create_node_response()
        elif action_name == "GetEnterpriseSyncMetaData":
            response.get_value.return_value = enterprise_sync_data
        else:
            response.get_value.return_value = None
        return response

    return side_effect


@patch(
    'FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission')
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

    with patch.object(facade.notification_controller.domain_controller, 'execute_sub_action',
                      side_effect=make_domain_sub_action_side_effect()):
        facade.mission_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']


@patch(
    'FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_log')
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

    with patch.object(facade.notification_controller.domain_controller, 'execute_sub_action',
                      side_effect=make_domain_sub_action_side_effect()):
        facade.mission_log_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']


@patch(
    'FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission_change')
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

    with patch.object(facade.notification_controller.domain_controller, 'execute_sub_action',
                      side_effect=make_domain_sub_action_side_effect(enterprise_sync_data=enterprise_sync_data)):
        facade.mission_content_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']


@patch(
    'FreeTAKServer.components.extended.mission.controllers.mission_persistence_controller.MissionPersistenceController.get_mission_cot')
def test_cot_created_notification(get_mission_cot_mock):
    """test the send_cot_created_notification action in the mission_notification_controller
    """
    setup = ComponentTest(TEST_COT_CREATED_NOTIFICATION_SCHEMA, mock_sub_actions=False, include_base_components=True)

    facade = Mission(ObjectFactory.get_instance("SyncActionMapper"), setup.request, setup.response, None)

    facade.initialize(setup.request, setup.response)

    mission = create_test_mission()

    cot = create_mission_cot()

    mission.cots.append(cot)

    get_mission_cot_mock.return_value = cot

    setup.request.set_value('mission_cot_id', "test")

    def notification_sub_action_side_effect(action_name):
        response = MagicMock()
        if action_name == "GetCoT":
            response.get_value.return_value = MagicMock()
        else:
            response.get_value.return_value = None
        return response

    with patch.object(facade.notification_controller.domain_controller, 'execute_sub_action',
                      side_effect=make_domain_sub_action_side_effect()), \
            patch.object(facade.notification_controller, 'execute_sub_action',
                         side_effect=notification_sub_action_side_effect):
        facade.send_cot_created_notification(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']