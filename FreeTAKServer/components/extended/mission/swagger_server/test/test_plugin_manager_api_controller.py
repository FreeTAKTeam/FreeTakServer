# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_collection_plugin_info import ApiResponseCollectionPluginInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPluginManagerApiController(BaseTestCase):
    """PluginManagerApiController integration test stubs"""

    def test_change_all_plugin_started_status(self):
        """Test case for change_all_plugin_started_status

        
        """
        query_string = [('status', true)]
        response = self.client.open(
            '/Marti/api/plugins/info/all/started',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_change_plugin_archive_setting(self):
        """Test case for change_plugin_archive_setting

        
        """
        query_string = [('name', 'name_example'),
                        ('archive_enabled', true)]
        response = self.client.open(
            '/Marti/api/plugins/info/archive',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_change_plugin_enabled_setting(self):
        """Test case for change_plugin_enabled_setting

        
        """
        query_string = [('name', 'name_example'),
                        ('status', true)]
        response = self.client.open(
            '/Marti/api/plugins/info/enabled',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_change_plugin_started_status(self):
        """Test case for change_plugin_started_status

        
        """
        query_string = [('name', 'name_example'),
                        ('status', true)]
        response = self.client.open(
            '/Marti/api/plugins/info/started',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_plugin_info(self):
        """Test case for get_all_plugin_info

        
        """
        response = self.client.open(
            '/Marti/api/plugins/info/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
