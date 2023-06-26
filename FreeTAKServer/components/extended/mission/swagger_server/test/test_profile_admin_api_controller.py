# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_list_profile import ApiResponseListProfile  # noqa: E501
from swagger_server.models.api_response_list_profile_directory import ApiResponseListProfileDirectory  # noqa: E501
from swagger_server.models.api_response_list_profile_file import ApiResponseListProfileFile  # noqa: E501
from swagger_server.models.api_response_list_string import ApiResponseListString  # noqa: E501
from swagger_server.models.api_response_profile import ApiResponseProfile  # noqa: E501
from swagger_server.models.api_response_profile_file import ApiResponseProfileFile  # noqa: E501
from swagger_server.models.name_file_body import NameFileBody  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProfileAdminApiController(BaseTestCase):
    """ProfileAdminApiController integration test stubs"""

    def test_add_file(self):
        """Test case for add_file

        
        """
        body = NameFileBody()
        query_string = [('filename', 'filename_example')]
        response = self.client.open(
            '/Marti/api/device/profile/{name}/file'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_profile(self):
        """Test case for create_profile

        
        """
        query_string = [('group', '[]')]
        response = self.client.open(
            '/Marti/api/device/profile/{name}'.format(name='name_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_directories(self):
        """Test case for delete_directories

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/directories'.format(name='name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_file(self):
        """Test case for delete_file

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/file/{id}'.format(name='name_example', id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_profile(self):
        """Test case for delete_profile

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{id}'.format(id=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_profile(self):
        """Test case for get_all_profile

        
        """
        response = self.client.open(
            '/Marti/api/device/profile',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_directories(self):
        """Test case for get_directories

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/directories'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_file1(self):
        """Test case for get_file1

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/file/{id}'.format(name='name_example', id=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_files(self):
        """Test case for get_files

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/files'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_profile(self):
        """Test case for get_profile

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_valid_directories(self):
        """Test case for get_valid_directories

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/directories',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_send_profile(self):
        """Test case for send_profile

        
        """
        body = ['body_example']
        response = self.client.open(
            '/Marti/api/device/profile/{name}/send'.format(name='name_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_directories(self):
        """Test case for update_directories

        
        """
        response = self.client.open(
            '/Marti/api/device/profile/{name}/directories/{directories}'.format(name='name_example', directories='directories_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_profile(self):
        """Test case for update_profile

        
        """
        body = Profile()
        response = self.client.open(
            '/Marti/api/device/profile/{name}'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
