import json
import pathlib
import uuid
from unittest.mock import MagicMock, Mock

from FreeTAKServer.core.configuration.MainConfig import MainConfig

from digitalpy.core.main.DigitalPy import DigitalPy
from digitalpy.core.main.controller import Controller
from digitalpy.core.zmanager.impl.default_request import DefaultRequest
from digitalpy.core.zmanager.impl.default_response import DefaultResponse
from digitalpy.core.component_management.impl.component_registration_handler import ComponentRegistrationHandler


class ComponentTest(DigitalPy):

    def __init__(self, test_schema, mock_sub_actions= True, include_base_components=False) -> None:
        super().__init__()

        self.test_obj = self.parse_schema(test_schema)

        # instnatiate request and response objects
        self.request, self.response = self.get_request_response_from_test_obj()

        if mock_sub_actions:
            # mock the execute sub action method in the controller class
            self.mock_controller_execute_sub_action(self.response)

        if include_base_components:
            # register the base components
            self.register_core_components()

        # get a mock node object
        self.mock_node = self.get_mock_node()

    def register_core_components(self):
        """this method is responsible for registering all FTS components"""
        config = MainConfig.instance()

        self.configuration.add_configuration(
            str(
                pathlib.PurePath(
                    str(config.MainPath),
                    "configuration",
                    "routing",
                    "action_mapping.ini",
                )
            ),
        )

        super().register_components()
        
        # register the internal components
        internal_components = ComponentRegistrationHandler.discover_components(
            component_folder_path=pathlib.PurePath(
                config.InternalComponentsPath
            ),
        )

        for internal_component in internal_components:
            ComponentRegistrationHandler.register_component(
                internal_component,
                config.InternalComponentsImportRoot,
                self.configuration,
            )

        # register the core components
        core_components = ComponentRegistrationHandler.discover_components(
            component_folder_path=pathlib.PurePath(
                config.CoreComponentsPath
            ),
        )

        for core_component in core_components:
            ComponentRegistrationHandler.register_component(
                core_component,
                config.CoreComponentsImportRoot,
                self.configuration,
            )

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