# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_server_config import ApiResponseServerConfig  # noqa: E501
from swagger_server.models.version_info import VersionInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestVersionApiController(BaseTestCase):
    """VersionApiController integration test stubs"""

    def test_get_node_id(self):
        """Test case for get_node_id

        
        """
        response = self.client.open(
            '/Marti/api/node/id',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_version(self):
        """Test case for get_version

        
        """
        response = self.client.open(
            '/Marti/api/version',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_version_config(self):
        """Test case for get_version_config

        
        """
        response = self.client.open(
            '/Marti/api/version/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_version_info(self):
        """Test case for get_version_info

        
        """
        response = self.client.open(
            '/Marti/api/version/info',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
