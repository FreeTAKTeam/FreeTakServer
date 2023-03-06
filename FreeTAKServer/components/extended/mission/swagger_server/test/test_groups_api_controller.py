# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_collection_group import ApiResponseCollectionGroup  # noqa: E501
from swagger_server.models.api_response_group import ApiResponseGroup  # noqa: E501
from swagger_server.models.api_response_sorted_set_user import ApiResponseSortedSetUser  # noqa: E501
from swagger_server.models.api_response_user_groups import ApiResponseUserGroups  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGroupsApiController(BaseTestCase):
    """GroupsApiController integration test stubs"""

    def test_get_all_groups(self):
        """Test case for get_all_groups

        
        """
        query_string = [('use_cache', false),
                        ('send_latest_sa', false)]
        response = self.client.open(
            '/Marti/api/groups/all',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_users2(self):
        """Test case for get_all_users2

        
        """
        response = self.client.open(
            '/Marti/api/users/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_group(self):
        """Test case for get_group

        
        """
        response = self.client.open(
            '/Marti/api/groups/{name}/{direction}'.format(name='name_example', direction='direction_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_group_cache_enabled(self):
        """Test case for get_group_cache_enabled

        
        """
        response = self.client.open(
            '/Marti/api/groups/groupCacheEnabled',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user(self):
        """Test case for get_user

        
        """
        response = self.client.open(
            '/Marti/api/users/{connectionId}'.format(connection_id='connection_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
