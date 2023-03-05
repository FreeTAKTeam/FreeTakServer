from unittest.mock import patch

from FreeTAKServer.core.cot_management.cot_management_facade import CotManagement
from tests.test_components.misc import ComponentTest
from tests.test_components.test_cot_manager.test_cot_manager_schemas import (
    TEST_CONNECTION_SCHEMA, TEST_CREATE_REPEATED_MESSAGE_SCHEMA,
    TEST_DELETE_NON_EXISTENT_REPEATED_MESSAGE_SCHEMA,
    TEST_DELETE_REPEATED_MESSAGE_SCHEMA, TEST_GET_REPEATED_MESSAGES_SCHEMA
)


# patch the persistency output
@patch('pickle.dump')
@patch('pickle.load')
def test_connection(mock_load, mock_dump):
    """test the connection action in the cot manager
    """
    setup = ComponentTest(TEST_CONNECTION_SCHEMA)

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(setup.mock_node.get_oid()): setup.mock_node}

    # instantiate the facade
    facade = CotManagement(None, setup.request, setup.response, None)

    # initialize the facade
    facade.initialize(setup.request, setup.response)

    # call the connection method from the facade
    facade.connection(**setup.request.get_values())

    # assert that the next action is publish
    assert setup.response.get_action() == setup.test_obj['response']['action']

    # assert the message value is correct
    setup.assert_schema_to_response_val(setup.test_obj['response']['values'])

@patch('pickle.dump')
@patch('pickle.load')
def test_get_repeated_messages(mock_load, mock_dump):

    setup = ComponentTest(TEST_GET_REPEATED_MESSAGES_SCHEMA)

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(setup.mock_node.get_oid()): setup.mock_node}

    # instantiate the facade
    facade = CotManagement(None, setup.request, setup.response, None)

    # initialize the facade
    facade.initialize(setup.request, setup.response)

    # call the get_repeated_messages method from the facade
    facade.get_repeated_messages(**setup.request.get_values())

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert setup.response.get_action() == setup.test_obj['response']['action']

    # assert the message value is correct
    setup.assert_schema_to_response_val(setup.test_obj['response']['values'])

@patch('pickle.dump')
@patch('pickle.load')
def test_create_repeated_message(mock_load, mock_dump):

    setup = ComponentTest(TEST_CREATE_REPEATED_MESSAGE_SCHEMA)

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(setup.mock_node.get_oid()): setup.mock_node}

    # instantiate the facade
    facade = CotManagement(None, setup.request, setup.response, None)

    # initialize the facade
    facade.initialize(setup.request, setup.response)

    # call the create repeated message method from the facade
    facade.create_repeated_message(**setup.request.get_values())

    # assert that the next action is CreateRepeatedMessage
    assert setup.response.get_action() == setup.test_obj['response']['action']

    # assert the success value is correct
    setup.assert_schema_to_response_val(setup.test_obj['response']['values'])

@patch('pickle.dump')
@patch('pickle.load')
def test_delete_repeated_message(mock_load, mock_dump):

    setup = ComponentTest(TEST_DELETE_REPEATED_MESSAGE_SCHEMA)

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(setup.mock_node.get_oid()): setup.mock_node}

    # instantiate the facade
    facade = CotManagement(None, setup.request, setup.response, None)

    # initialize the facade
    facade.initialize(setup.request, setup.response)

    # call the delete_repeated_messages method from the facade
    facade.delete_repeated_message(**setup.request.get_values())

    # assert that the next action is the same
    assert setup.response.get_action() == setup.test_obj['response']['action']

    # assert the success value is correct
    setup.assert_schema_to_response_val(setup.test_obj['response']['values'])

@patch('pickle.dump')
@patch('pickle.load')
def test_delete_non_existent_repeated_message(mock_load, mock_dump):
    setup = ComponentTest(TEST_DELETE_NON_EXISTENT_REPEATED_MESSAGE_SCHEMA)

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(setup.mock_node.get_oid()): setup.mock_node}

    # instantiate the facade
    facade = CotManagement(None, setup.request, setup.response, None)

    # initialize the facade
    facade.initialize(setup.request, setup.response)

    # call the delete_repeated_messages method from the facade
    facade.delete_repeated_message(**setup.request.get_values())

    assert setup.response.get_action() == setup.test_obj['response']['action']

    # assert the success value is correct
    setup.assert_schema_to_response_val(setup.test_obj['response']['values'])
