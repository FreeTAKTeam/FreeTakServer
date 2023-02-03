import json
import uuid
from unittest.mock import MagicMock, Mock, patch

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.impl.default_request import DefaultRequest
from digitalpy.core.zmanager.impl.default_response import DefaultResponse

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

def get_mock_node_from_obj(obj: dict, oid = get_mock_oid()):
    mock_node = Mock()
    mock_node.get_oid.return_value = oid

    for key in obj:
        setattr(mock_node, key, obj[key])

    return mock_node

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

def assert_schema_to_response_val(response_schema_values, response):
    for key, value in response_schema_values.items():
        # assert that the value exists in component response
        assert response.get_value(key) is not None
        # assert that they are the correct type
        assert isinstance(response.get_value(key), type(value))

        # TODO if they are mock obj then only compare ids
        # assert that they are the same
        assert response.get_value(key) == value

def parse_schema(schema: str):
    return json.loads(schema)

def get_request_response_from_test_obj(test_obj):
    request = DefaultRequest()
    response = DefaultResponse()

    # if value is a node object, create mock node
    for key in test_obj['request']['values']:
        value = test_obj['request']['values'][key]
        if isinstance(value, list):
            test_obj['request']['values'][key] = r_convert_values_to_node(value)
        elif value['is_node']:
            test_obj['request']['values'][key] = get_mock_node_from_obj(value, value['oid'])

    # set request action and values
    request.set_action(test_obj['request']['action'])
    request.set_values(test_obj['request']['values'])

    # set response action
    response.set_action(test_obj['response']['action'])

    return request, response

def r_convert_values_to_node(value):
    base = value[0]

    if isinstance(base, list):
        r_convert_values_to_node(value[0])
        
    if isinstance(base, dict) and base['is_node']:
        return [get_mock_node_from_obj(base, base['oid'])]

    # assume value is list of non node items aka strings
    return value

test_connection_schema = """
{
    "request": {
        "values": {
            "connection": {
                "oid": "3b1a979c-a31b-11ed-a8fc-0242ac120002",
                "service_id": "test_service",
                "protocol": "test_protocol",
                "is_node": true 
            }
        },
        "action": "connection"
    },
    "response": {
        "action": "publish",
        "values": {
            "message": [

            ]
        }
    },
    "node_id": "3b1a979c-a31b-11ed-a8fc-0242ac120002"
}
"""

# patch the persistency output
@patch('pickle.load')
def test_connection(mock_load):
    """test the connection action in the cot manager
    """
    test_obj = parse_schema(test_connection_schema)

    # instnatiate request and response objects
    request, response = get_request_response_from_test_obj(test_obj)

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node(oid=test_obj['node_id'])

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the connection method from the facade
    facade.connection(**request.get_values())

    # assert that the next action is publish
    assert response.get_action() == test_obj['response']['action']

    # assert the message value is correct
    assert_response_val('message', list, [mock_node], response)

test_get_repeated_messages_schema = """
{
    "request": {
        "values": {},
        "action": "GetRepeatedMessages"
    },
    "response":{
        "action": "GetRepeatedMessages"
    },
    "node_id": "672a39ee-a31d-11ed-a8fc-0242ac120002"
}
"""

@patch('pickle.load')
def test_get_repeated_messages(mock_load):

    test_obj = parse_schema(test_get_repeated_messages_schema)

    # instnatiate request and response objects
    request, response = get_request_response_from_test_obj(test_obj)

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node(oid=test_obj['node_id'])

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the get_repeated_messages method from the facade
    facade.get_repeated_messages(**request.get_values())

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert response.get_action() == test_obj['response']['action']

    # assert the message value is correct
    assert_response_val('message', list, [mock_node], response)

test_create_repeated_message_schema = """
{
    "request": {
        "values": {
            "message": [
                {
                    "oid": "59886b34-a31e-11ed-a8fc-0242ac120002",
                    "is_node": true
                }
            ]
        },
        "action": "CreateRepeatedMessage"
    },
    "response": {
        "action": "CreateRepeatedMessage",
        "values": {
            "success": true
        }
    }
}
"""

@patch('pickle.dump')
@patch('pickle.load')
def test_create_repeated_message(mock_load, mock_dump):

    test_obj = parse_schema(test_create_repeated_message_schema)

    # instnatiate request and response objects
    request, response = get_request_response_from_test_obj(test_obj)

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {}

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the create repeated message method from the facade
    facade.create_repeated_message(**request.get_values())

    # assert that the next action is CreateRepeatedMessage
    assert response.get_action() == test_obj['response']['action']

    # assert the success value is correct
    assert_schema_to_response_val(test_obj['response']['values'], response)

test_delete_repeated_message_schema = """
{
    "request": {
        "values": {
            "ids": [
                "329f80aa-a2f8-11ed-a8fc-0242ac120002"
            ]
        },
        "action": "DeleteRepeatedMessage"
    },
    "response": {
        "action": "DeleteRepeatedMessage"
    },
    "node_id": "329f80aa-a2f8-11ed-a8fc-0242ac120002"
}
"""

@patch('pickle.dump')
@patch('pickle.load')
def test_delete_repeated_message(mock_load, mock_dump):
    # parse object from schema
    test_obj = parse_schema(test_delete_repeated_message_schema)

    # instantiate request and response objects
    request, response = get_request_response_from_test_obj(test_obj)
    
    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node(oid=test_obj['node_id'])

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the delete_repeated_messages method from the facade
    facade.delete_repeated_message(**request.get_values())

    # assert that the next action is the same
    assert response.get_action() == test_obj['response']['action']

    # assert the success value is correct
    assert_response_val('success', bool, True, response)

test_delete_non_existent_repeated_message = """
{
    "request": {
        "values": {
            "ids": ["329f80aa-a2f8-11ed-a8fc-0242ac120002"]
        },
        "action": "DeleteRepeatedMessage"
    },
    "response": {
        "action": "DeleteRepeatedMessage"
    },
    "node_id": "329f80aa-a2f8-11ed-a8fc-0242ac120002"
}
"""

@patch('pickle.dump')
@patch('pickle.load')
def test_delete_non_existent_repeated_message(mock_load, mock_dump):
    # parse object from schema
    test_obj = parse_schema(test_delete_repeated_message_schema)

    # instantiate request and response objects
    request, response = get_request_response_from_test_obj(test_obj)

    # # instnatiate request and response objects
    # request, response = instantiate_request_response("DeleteRepeatedMessage")
    
    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {}

    request.set_value("ids", [str(mock_node.get_oid())])

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the delete_repeated_messages method from the facade
    facade.delete_repeated_message(**request.get_values())

    assert response.get_action() == test_obj['response']['action']
    # assert the success value is correct
    assert_response_val('success', bool, True, response)
