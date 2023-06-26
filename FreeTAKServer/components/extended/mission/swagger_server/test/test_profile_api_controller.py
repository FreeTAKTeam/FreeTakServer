# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestProfileApiController(BaseTestCase):
    """ProfileApiController integration test stubs"""

    def test_device_get_profile_directory_content(self):
        """Test case for device_get_profile_directory_content

        
        """
        query_string = [('relative_path', 'relative_path_example'),
                        ('sync_secago', -1),
                        ('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/device/profile/tool/{toolName}/file'.format(tool_name='tool_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_connection_time_profiles(self):
        """Test case for get_connection_time_profiles

        
        """
        query_string = [('sync_secago', 789),
                        ('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/device/profile/connection',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_enrollment_time_profiles(self):
        """Test case for get_enrollment_time_profiles

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/tls/profile/enrollment',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_profile_mp(self):
        """Test case for get_profile_mp

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/missionpackage'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_tool_profiles(self):
        """Test case for get_tool_profiles

        
        """
        query_string = [('sync_secago', -1),
                        ('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/device/profile/tool/{toolName}'.format(tool_name='tool_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_head_profile_mp(self):
        """Test case for head_profile_mp

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/missionpackage'.format(name='name_example'),
            method='HEAD')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_tls_get_profile_directory_content(self):
        """Test case for tls_get_profile_directory_content

        
        """
        query_string = [('relative_path', 'relative_path_example'),
                        ('sync_secago', -1),
                        ('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/tls/profile/tool/{toolName}/file'.format(tool_name='tool_name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
