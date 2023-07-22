from unittest.mock import Mock, patch, MagicMock
import uuid
import pickle
from typing import Dict
from digitalpy.core.zmanager.impl.default_request import DefaultRequest
from digitalpy.core.zmanager.impl.default_response import DefaultResponse
from digitalpy.core.main.controller import Controller
from digitalpy.core.main.object_factory import ObjectFactory
from digitalpy.core.parsing.load_configuration import Configuration

from FreeTAKServer.core.cot_management.cot_management_facade import CotManagement

def setup():
    pass

def mock_controller_execute_sub_action(sub_response = Mock()):
    Controller.execute_sub_action = Mock(return_value=sub_response)

def get_mock_oid(oid_str = str(uuid.uuid1())):
    mock_oid = MagicMock()
    mock_oid.__str__.return_value = oid_str
    return 

def get_mock_node(oid = get_mock_oid()):
    mock_node = Mock()
    mock_node.get_oid.return_value = oid
    return mock_node

def get_mock_event(mock_node = get_mock_node(), uid = '', type = ''):
    mock_node.uid = uid
    mock_node.type = type
    return mock_node

def get_mock_repeated_message(node):
    mock_repeated_message = Mock()
    mock_repeated_message.message = node
    return mock_repeated_message
    
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
    if len(persistency_save_method.mock_calls[0].args)>0:
        assert value[0] in list(persistency_save_method.mock_calls[0].args[0])
    elif len(persistency_save_method.mock_calls[0].kwargs)>0:
        assert value[0] in persistency_save_method.mock_calls[0].kwargs.values()

# patch the persistency output
@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_connection_direct(mock_get_repeated_messages):
    """test the connection action in the cot manager
    """
    # instnatiate request and response objects
    request, response = instantiate_request_response("connection")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # get a mock RepeatedMessage object
    repeated_message = get_mock_repeated_message(mock_node)

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = [repeated_message]

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
    
# patch the persistency output
@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_connection_execute(mock_get_repeated_messages):
    """test the connection action in the cot manager
    """
    # instnatiate request and response objects
    request, response = instantiate_request_response("connection")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # get a mock RepeatedMessage object
    repeated_message = get_mock_repeated_message(mock_node)

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = [repeated_message]

    # instantiate a mock connection object
    mock_connection = get_mock_connection()

    # set the content of the connection value to be a mock connection
    request.set_value("connection", mock_connection)

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the connection method from the facade
    facade.execute("connection")

    # assert that the next action is publish
    assert response.get_action() == "publish"
    # assert the message value is correct
    assert_response_val('message', list, [mock_node], response)

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_get_repeated_messages(mock_get_repeated_messages):

    # instnatiate request and response objects
    request, response = instantiate_request_response("GetRepeatedMessages")

    request.set_value("extra", True)

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # get a mock RepeatedMessage object
    repeated_message = get_mock_repeated_message(mock_node)

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = [repeated_message]

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
    # assert the extra value was passed through
    assert_response_val('extra', bool, True, response)

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_get_repeated_messages_execute(mock_get_repeated_messages):

    # instnatiate request and response objects
    request, response = instantiate_request_response("GetRepeatedMessages")

    request.set_value("extra", True)

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # get a mock RepeatedMessage object
    repeated_message = get_mock_repeated_message(mock_node)

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = [repeated_message]

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the get_repeated_messages method from the facade
    facade.execute("get_repeated_messages")

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert response.get_action() == "GetRepeatedMessages"
    # assert the message value is correct
    assert_response_val('message', list, [mock_node], response)
    # assert the extra value was passed through
    assert_response_val('extra', bool, True, response)

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.create_repeated_message')
@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_create_repeated_message(mock_get_repeated_messages, mock_create_repeated_message):

    # instnatiate request and response objects
    request, response = instantiate_request_response("CreateRepeatedMessage")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_event = get_mock_event()

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = []

    # set the content of the message value to be a list containing one mocked node
    request.set_value("message", [mock_event])

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
    assert_saved(mock_create_repeated_message, [mock_event, str(mock_event.uid)])

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.create_repeated_message')
@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_create_repeated_message_execute(mock_get_repeated_messages, mock_create_repeated_message):

    # instnatiate request and response objects
    request, response = instantiate_request_response("CreateRepeatedMessage")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_event = get_mock_event()

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = []

    # set the content of the message value to be a list containing one mocked node
    request.set_value("message", [mock_event])

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the create repeated message method from the facade
    facade.execute("create_repeated_message")

    # assert that the next action is CreateRepeatedMessage
    assert response.get_action() == "CreateRepeatedMessage"
    # assert the success value is correct
    assert_response_val('success', bool, True, response)
    # assert that the node was saved
    assert_saved(mock_create_repeated_message, [mock_event, str(mock_event.uid)])

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.delete_repeated_message')
@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_delete_repeated_message(mock_get_repeated_messages, mock_delete_repeated_message):

    # instnatiate request and response objects
    request, response = instantiate_request_response("DeleteRepeatedMessage")
    
    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = [mock_node]

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
    # delete was called with the node id
    assert_saved(mock_delete_repeated_message, [str(mock_node.get_oid())])

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.delete_repeated_message')
@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_delete_repeated_message_execute(mock_get_repeated_messages, mock_delete_repeated_message):

    # instnatiate request and response objects
    request, response = instantiate_request_response("DeleteRepeatedMessage")
    
    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = [mock_node]

    request.set_value("ids", [str(mock_node.get_oid())])

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the delete_repeated_messages method from the facade
    facade.execute("delete_repeated_message")

    assert response.get_action() == "DeleteRepeatedMessage"
    # assert the success value is correct
    assert_response_val('success', bool, True, response)
    # assert that the was deleted and an empty dictionary was saved instead
    assert_saved(mock_delete_repeated_message, [str(mock_node.get_oid())])

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.delete_repeated_message')
@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.get_all_repeated_messages')
def test_delete_non_existent_repeated_message(mock_get_repeated_messages, mock_delete_repeated_message):

    # instnatiate request and response objects
    request, response = instantiate_request_response("DeleteRepeatedMessage")
    
    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # get a mock node object
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_get_repeated_messages.return_value = [mock_node]

    request.set_value("ids", [str(mock_node.get_oid())])

    request.set_value("ids", [str(mock_node.get_oid())])

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the delete_repeated_messages method from the facade
    facade.execute("delete_repeated_message")

    assert response.get_action() == "DeleteRepeatedMessage"
    # assert the success value is correct
    assert_response_val('success', bool, True, response)
    # assert that the was deleted and an empty dictionary was saved instead
    assert_saved(mock_delete_repeated_message, [str(mock_node.get_oid())])

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.create_repeated_message')
def test_create_geo_object(create_repeated_message):

    # instnatiate request and response objects
    request, response = instantiate_request_response("CreateGeoObject")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the get_repeated_messages method from the facade
    facade.create_geo_object(**request.get_values())

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert response.get_action() == "CreateNode"
    # assert the message object_class_name is correct
    assert_response_val('object_class_name', str, "Event", response)
    # assert the configuration is of correct type
    assert isinstance(response.get_value("configuration"), Configuration)

@patch('FreeTAKServer.core.cot_management.controllers.cot_management_repeater_persistence.CotManagementRepeaterPersistence.create_repeated_message')
def test_create_geo_object_execute(mock_create_repeated_message):

    # instnatiate request and response objects
    request, response = instantiate_request_response("CreateGeoObject")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the get_repeated_messages method from the facade
    facade.execute("create_geo_object")

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert response.get_action() == "CreateNode"
    # assert the message object_class_name is correct
    assert_response_val('object_class_name', str, "Event", response)
    # assert the configuration is of correct type
    assert isinstance(response.get_value("configuration"), Configuration)

def test_delete_geo_object():
        # instnatiate request and response objects
    request, response = instantiate_request_response("DeleteGeoObject")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the get_repeated_messages method from the facade
    facade.delete_geo_object(**request.get_values())

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert response.get_action() == "CreateNode"
    # assert the message object_class_name is correct
    assert_response_val('object_class_name', str, "Event", response)
    # assert the configuration is of correct type
    assert isinstance(response.get_value("configuration"), Configuration)

def test_delete_geo_object_execute():
        # instnatiate request and response objects
    request, response = instantiate_request_response("DeleteGeoObject")

    # mock the execute sub action method in the controller class
    mock_controller_execute_sub_action(response)

    # instantiate the facade
    facade = CotManagement(None, request, response, None)

    # initialize the facade
    facade.initialize(request, response)

    # call the get_repeated_messages method from the facade
    facade.execute("delete_geo_object")

    # assert that the next action is GetRepeatedMessages thus resulting in no further actions being called
    assert response.get_action() == "CreateNode"
    # assert the message object_class_name is correct
    assert_response_val('object_class_name', str, "Event", response)
    # assert the configuration is of correct type
    assert isinstance(response.get_value("configuration"), Configuration)