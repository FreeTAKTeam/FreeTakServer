# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_integer import ApiResponseInteger  # noqa: E501
from swagger_server.models.api_response_sorted_set_ldap_group import ApiResponseSortedSetLdapGroup  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLdapApiController(BaseTestCase):
    """LdapApiController integration test stubs"""

    def test_get_group_prefix(self):
        """Test case for get_group_prefix

        
        """
        response = self.client.open(
            '/Marti/api/groupprefix',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ldap_group_members(self):
        """Test case for get_ldap_group_members

        
        """
        query_string = [('group_name_filter', 'group_name_filter_example')]
        response = self.client.open(
            '/Marti/api/groups/members',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ldap_groups(self):
        """Test case for get_ldap_groups

        
        """
        query_string = [('group_name_filter', 'group_name_filter_example')]
        response = self.client.open(
            '/Marti/api/groups',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
