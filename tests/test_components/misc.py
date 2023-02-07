import json
import uuid
from unittest.mock import MagicMock, Mock

from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.impl.default_request import DefaultRequest
from digitalpy.core.zmanager.impl.default_response import DefaultResponse


class ComponentTest():

    def __init__(self, test_schema) -> None:
        self.test_obj = self.parse_schema(test_schema)

        # instnatiate request and response objects
        self.request, self.response = self.get_request_response_from_test_obj()

        # mock the execute sub action method in the controller class
        self.mock_controller_execute_sub_action(self.response)

        # get a mock node object
        self.mock_node = self.get_mock_node()

    def mock_controller_execute_sub_action(self, sub_response = Mock()):
        Controller.execute_sub_action = Mock(return_value=sub_response)

    def get_mock_oid(self, oid_str = str(uuid.uuid1())):
        mock_oid = MagicMock()
        mock_oid.__str__.return_value = oid_str
        return mock_oid

    def get_mock_node(self, oid = None):
        mock_node = Mock()

        if oid is None:
            mock_node.get_oid.return_value = self.get_mock_oid()
        else:
            mock_node.get_oid.return_value = oid

        return mock_node

    def get_mock_node_from_obj(self, obj: dict, oid = None):
        mock_node = Mock()

        if oid is None:
            mock_node.get_oid.return_value = self.get_mock_node()
        else:
            mock_node.get_oid.return_value = oid

        for key in obj:
            setattr(mock_node, key, obj[key])

        return mock_node

    def assert_response_val(self, value_name, value_type, value_content):
        assert self.response.get_value(value_name) != None
        assert isinstance(self.response.get_value(value_name), value_type)
        assert self.response.get_value(value_name) == value_content

    def assert_schema_to_response_val(self, response_schema_values):
        for key, value in response_schema_values.items():
            # assert that the value exists in component response
            assert self.response.get_value(key) is not None
            # assert that they are the correct type
            assert isinstance(self.response.get_value(key), type(value))

            if isinstance(value, list):
                # assert return value contains something
                assert len(value) == len(self.response.get_value(key))
            else:
                # assert that they are the same
                assert self.response.get_value(key) == value

    def parse_schema(self, schema: str):
        return json.loads(schema)

    def get_request_response_from_test_obj(self):
        request = DefaultRequest()
        response = DefaultResponse()

        # if value is a node object, create mock node
        for key, value in self.test_obj['request']['values'].items():
            if isinstance(value, list):
                self.test_obj['request']['values'][key] = self.r_convert_values_to_node(value)
            elif isinstance(value, dict) and value['is_node']:
                self.test_obj['request']['values'][key] = self.get_mock_node_from_obj(value, value.get('oid', self.get_mock_oid()))

        for key, value in self.test_obj['response']['values'].items():
            if isinstance(value, list):
                self.test_obj['response']['values'][key] = self.r_convert_values_to_node(value)
            elif isinstance(value, dict) and value['is_node']:
                self.test_obj['response']['values'][key] = self.get_mock_node_from_obj(value, value.get('oid', self.get_mock_oid()))

        # set request action and values
        request.set_action(self.test_obj['request']['action'])
        request.set_values(self.test_obj['request']['values'])

        # set response action
        response.set_action(self.test_obj['response']['action'])

        return request, response

    def r_convert_values_to_node(self, value):
        base = value[0]

        if isinstance(base, list):
            self.r_convert_values_to_node(value[0])
        
        if isinstance(base, dict) and base['is_node']:
            return [self.get_mock_node_from_obj(base, base.get('oid', self.get_mock_oid()))]

        # assume value is list of non node items aka strings
        return value