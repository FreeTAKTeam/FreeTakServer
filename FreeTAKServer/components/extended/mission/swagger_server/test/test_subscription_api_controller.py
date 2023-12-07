# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_set_subscription_info import ApiResponseSetSubscriptionInfo  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.api_response_subscription_info import ApiResponseSubscriptionInfo  # noqa: E501
from swagger_server.models.filter import Filter  # noqa: E501
from swagger_server.models.group import Group  # noqa: E501
from swagger_server.models.tmp_static_sub import TmpStaticSub  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSubscriptionApiController(BaseTestCase):
    """SubscriptionApiController integration test stubs"""

    def test_add_subscription(self):
        """Test case for add_subscription

        
        """
        body = TmpStaticSub()
        response = self.client.open(
            '/Marti/api/subscriptions/add',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_filter(self):
        """Test case for delete_filter

        
        """
        response = self.client.open(
            '/Marti/api/subscriptions/{clientUid}/filter'.format(client_uid='client_uid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_subscription(self):
        """Test case for delete_subscription

        
        """
        response = self.client.open(
            '/Marti/api/subscriptions/delete/{uid}'.format(uid='uid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_subscriptions(self):
        """Test case for get_all_subscriptions

        
        """
        query_string = [('sort_by', 'CALLSIGN'),
                        ('direction', 'ASCENDING'),
                        ('page', -1),
                        ('limit', -1)]
        response = self.client.open(
            '/Marti/api/subscriptions/all',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_groups_updated(self):
        """Test case for groups_updated

        
        """
        response = self.client.open(
            '/Marti/api/groups/update/{username}'.format(username='username_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_active_groups(self):
        """Test case for set_active_groups

        
        """
        body = [56]
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/groups/activebits',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_active_groups1(self):
        """Test case for set_active_groups1

        
        """
        body = [Group()]
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/groups/active',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_filter(self):
        """Test case for set_filter

        
        """
        body = Filter()
        response = self.client.open(
            '/Marti/api/subscriptions/{clientUid}/filter'.format(client_uid='client_uid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/xml')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_toggle_incognito(self):
        """Test case for toggle_incognito

        
        """
        response = self.client.open(
            '/Marti/api/subscriptions/incognito/{uid}'.format(uid='uid_example'),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
