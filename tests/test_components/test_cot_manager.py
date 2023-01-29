from unittest.mock import Mock, patch, MagicMock
import uuid
import pickle
from typing import Dict
from digitalpy.core.zmanager.impl.default_request import DefaultRequest
from digitalpy.core.zmanager.impl.default_response import DefaultResponse
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
from FreeTAKServer.core.cot_management.cot_management_facade import CotManagement

def setup():
    pass

def mock_controller_execute_sub_action(sub_response = Mock()):
    Controller.execute_sub_action = Mock(return_value=sub_response)

def get_mock_oid(oid_str = str(uuid.uuid1())):
    mock_oid = MagicMock()
    mock_oid.__str__.return_value = oid_str
    return mock_oid

def get_mock_node(oid = get_mock_oid()):
    mock_node = Mock()
    mock_node.get_oid.return_value = oid
    return mock_node

def get_mock_connection(node = get_mock_node(), service_id = "test-service", protocol = "test-protocol"):
    mock_connection = node
    mock_connection.service_id = "test_service"
    mock_connection.protocol = "test_protocol"
    return mock_connection

def instantiate_request_response(action):
    request = DefaultRequest()
    response = DefaultResponse()

    request.set_action(action)
    response.set_action(action)

    return request, response

def assert_response_val(value_name, value_type, value_content, response):
    assert response.get_value(value_name) != None
    assert isinstance(response.get_value(value_name), value_type)
    assert response.get_value(value_name) == value_content

def assert_saved(persistency_save_method: callable, value):
    assert value in persistency_save_method.mock_calls[0].args

# patch the persistency output
@patch('pickle.load')
def test_connection(mock_load):
    """test the connection action in the cot manager
    """
    # instnatiate request and response objects
    request, response = instantiate_request_response("connection")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    # instantiate a mock connection object
    mock_connection = get_mock_connection()

    # set the content of the connection value to be a mock connection
    request.set_value("connection", mock_connection)

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the connection method from the facade
    facade.connection(**request.get_values())

    # assert that the next action is publish
    assert response.get_action() == "publish"
    # assert the message value is correct
    assert_response_val('message', list, [mock_node], response)
    
@patch('pickle.load')
def test_get_repeated_messages(mock_load):

    # instnatiate request and response objects
    request, response = instantiate_request_response("GetRepeatedMessages")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the get_repeated_messages method from the facade
    facade.get_repeated_messages(**request.get_values())

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert response.get_action() == "GetRepeatedMessages"
    # assert the message value is correct
    assert_response_val('message', list, [mock_node], response)

@patch('pickle.dump')
@patch('pickle.load')
def test_create_repeated_message(mock_load, mock_dump):

    # instnatiate request and response objects
    request, response = instantiate_request_response("CreateRepeatedMessage")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {}

    # set the content of the message value to be a list containing one mocked node
    request.set_value("message", [mock_node])

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the create repeated message method from the facade
    facade.create_repeated_message(**request.get_values())

    # assert that the next action is CreateRepeatedMessage
    assert response.get_action() == "CreateRepeatedMessage"
    # assert the success value is correct
    assert_response_val('success', bool, True, response)
    # assert that the node was saved
    assert_saved(mock_dump, {str(mock_node.get_oid()): mock_node})

@patch('pickle.dump')
@patch('pickle.load')
def test_delete_repeated_message(mock_load, mock_dump):

    # instnatiate request and response objects
    request, response = instantiate_request_response("DeleteRepeatedMessage")
    
    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    request.set_value("ids", [str(mock_node.get_oid())])

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the delete_repeated_messages method from the facade
    facade.delete_repeated_message(**request.get_values())

    assert response.get_action() == "DeleteRepeatedMessage"
    # assert the success value is correct
    assert_response_val('success', bool, True, response)
    # assert that the was deleted and an empty dictionary was saved instead
    assert_saved(mock_dump, {})
