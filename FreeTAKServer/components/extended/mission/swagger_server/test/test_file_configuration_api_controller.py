# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.file_configuration_model import FileConfigurationModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFileConfigurationApiController(BaseTestCase):
    """FileConfigurationApiController integration test stubs"""

    def test_get_file_configuration(self):
        """Test case for get_file_configuration

        
        """
        response = self.client.open(
            '/files/api/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_file_configuration(self):
        """Test case for set_file_configuration

        
        """
        body = FileConfigurationModel()
        response = self.client.open(
            '/files/api/config',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
