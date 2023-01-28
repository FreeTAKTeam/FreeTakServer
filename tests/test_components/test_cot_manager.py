from unittest.mock import Mock, patch, MagicMock
import uuid
import pickle
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

# patch the persistency output
@patch('pickle.load')
def test_connection(mock_load):

    request = DefaultRequest()
    response = DefaultResponse()

    mock_controller_execute_sub_action(response)

    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    mock_connection = get_mock_connection()

    request.set_value("connection", mock_connection)

    facade = CotManagement(None, request, response, None)

    facade.initialize(request, response)

    facade.connection(**request.get_values())

    assert response.get_action() == "publish"
    assert 'message' in response.get_values()
    assert len(response.get_value("message")) == 1
    assert response.get_value("message")[0] == mock_node

@patch('pickle.load')
def test_get_repeated_messages(mock_load):
    request = DefaultRequest()
    response = DefaultResponse()

    mock_controller_execute_sub_action(response)
    
    mock_node = get_mock_node()

    # define the output dictionary of the mocked persistency output
    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    facade = CotManagement(None, request, response, None)

    facade.initialize(request, response)

    facade.connection(**request.get_values())

    assert response.get_action() == "publish"
    assert 'message' in response.get_values()
    assert len(response.get_value("message")) == 1
    assert isinstance(response.get_value("message"), list)
    assert response.get_value("message")[0] == mock_node

@patch('pickle.load')
@patch('pickle.dump')
def test_create_repeated_message(self, mock_load, mock_dump):
    request = DefaultRequest()
    response = DefaultResponse()

    mock_controller_execute_sub_action(response)

    mock_node = get_mock_node()

    mock_load.return_value = {str(mock_node.get_oid()): mock_node}

    facade = CotManagement(None, request, response, None)

    facade.initialize(request, response)

    assert response.get_action() == "CreateRepeatedMessage"
    assert response.get_value('success')