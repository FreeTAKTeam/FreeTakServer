from unittest.mock import patch

from FreeTAKServer.components.extended.mission.mission_facade import Mission
from tests.test_components.misc import ComponentTest
from tests.test_components.test_mission_component.test_mission_subscription_schemas import TEST_GET_ALL_SUBSCRIPTIONS_SCHEMA

def mock_sqlalchemy_query_all(mock_query, mock_node):
    """mock the query.all method in sqlalchemy
    """
    mock_query.all.return_value = [mock_node]

def test_get_all_subscriptions():
    """test the get_all_subscriptions action in the mission component
    """
    setup = ComponentTest(TEST_GET_ALL_SUBSCRIPTIONS_SCHEMA)

    # instantiate the facade
    facade = Mission(None, setup.request, setup.response, None)

    # initialize the facade
    facade.initialize(setup.request, setup.response)

    # mock the query.all method in sqlalchemy
    mock_sqlalchemy_query_all(facade.subscription_controller.persistency_controller.ses.query, setup.mock_node)

    # call the get_all_subscriptions method from the facade
    facade.get_all_subscriptions(**setup.request.get_values())

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert setup.response.get_action() == setup.test_obj['response']['action']

    # assert the message value is correct
    setup.assert_schema_to_response_val(setup.test_obj['response']['values'])