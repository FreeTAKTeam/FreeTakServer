from unittest.mock import MagicMock, patch
from digitalpy.core.zmanager.impl.default_response import DefaultResponse
from FreeTAKServer.core.cot_management.cot_management_facade import CotManagement
from tests.test_components.misc import ComponentTest
from digitalpy.core.main.object_factory import ObjectFactory
from tests.test_components.test_cot_manager_component.test_cot_manager_general_controller_schema import TEST_MISSION_COT

@patch("FreeTAKServer.core.cot_management.controllers.cot_management_persistence_controller.CoTManagementPersistenceController.create_or_update_cot")
@patch("digitalpy.core.main.controller.Controller.execute_sub_action")
def test_handle_default_cot(
    execute_sub_action_mock,
    create_or_update_cot_mock
):
    setup = ComponentTest(TEST_MISSION_COT, mock_sub_actions=False, include_base_components=True)

    fake_response = DefaultResponse()

    fake_model_object = MagicMock()

    fake_model_object.uid = "test-uid"
    fake_model_object.type = "a-f-G-U-C"

    fake_model_object.detail = MagicMock()
    fake_model_object.detail.marti = MagicMock()

    fake_dest = MagicMock()
    fake_dest.mission = "mission-test"
    fake_dest.callsign = None

    fake_model_object.detail.marti.dest = [fake_dest]

    fake_response.set_value(
        "model_object",
        fake_model_object
    )

    execute_sub_action_mock.return_value = fake_response

    async_action_mapper_mock = MagicMock()

    facade = CotManagement(action_mapper= async_action_mapper_mock, sync_action_mapper=ObjectFactory.get_instance("SyncActionMapper"), request=setup.request, response=setup.response, configuration=None)

    facade.initialize(setup.request, setup.response)

    facade.default_cot_processor(**setup.request.get_values())

    # Check that appropriate values are set in the request and response
    assert setup.request.get_value("target_format") == "node"
    assert setup.response.get_action() == "publish"

    # Check if the sub-actions were executed with expected arguments
    async_action_mapper_mock.process_action.assert_called_with(setup.request, setup.response, False, protocol="XML")

    # Add more assertions as needed based on your specific expectations

    # Example of checking if recipients are set correctly
    recipients = setup.request.get_value("recipients")
    assert recipients == '*'