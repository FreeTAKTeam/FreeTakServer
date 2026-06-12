from unittest.mock import patch, MagicMock

from FreeTAKServer.components.extended.mission.mission_facade import Mission
from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.test_mission_subscription_schemas import TEST_GET_ALL_SUBSCRIPTIONS_SCHEMA


def test_get_all_subscriptions():
    """test the get_all_subscriptions action in the mission component
    """
    setup = ComponentTest(TEST_GET_ALL_SUBSCRIPTIONS_SCHEMA)

    # instantiate the facade
    facade = Mission(None, setup.request, setup.response, None)

    # initialize the facade
    facade.initialize(setup.request, setup.response)

    def sub_action_side_effect(action_name):
        response = MagicMock()
        if action_name == "serialize":
            response.get_value.return_value = ["{}"]
        elif action_name == "CreateNode":
            response.get_value.return_value = MagicMock()
        else:
            response.get_value.return_value = None
        return response

    with patch.object(
            facade.subscription_controller.persistency_controller,
            'get_all_subscriptions',
            return_value=[]
        ), \
        patch.object(
            facade.subscription_controller,
            'execute_sub_action',
            side_effect=sub_action_side_effect
        ), \
        patch.object(
            facade.subscription_controller.domain_controller,
            'execute_sub_action',
            side_effect=sub_action_side_effect
        ):
        facade.get_all_subscriptions(**setup.request.get_values())

    # assert the response action is correct
    assert setup.response.get_action() == setup.test_obj['response']['action']

    # assert mission_subscriptions is set
    setup.assert_schema_to_response_val(setup.test_obj['response']['values'])