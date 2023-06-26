# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.configuration import Configuration  # noqa: E501
from swagger_server.models.input import Input  # noqa: E501
from swagger_server.test import BaseTestCase


class TestConfigApiController(BaseTestCase):
    """ConfigApiController integration test stubs"""

    def test_get_cached_core_config(self):
        """Test case for get_cached_core_config

        
        """
        response = self.client.open(
            '/Marti/api/cachedConfig',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cached_input_config(self):
        """Test case for get_cached_input_config

        
        """
        response = self.client.open(
            '/Marti/api/cachedInputConfig',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_core_config(self):
        """Test case for get_core_config

        
        """
        response = self.client.open(
            '/Marti/api/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
