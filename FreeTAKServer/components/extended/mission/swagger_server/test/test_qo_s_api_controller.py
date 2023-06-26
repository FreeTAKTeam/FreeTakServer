# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_entry_integer_integer import ApiResponseEntryIntegerInteger  # noqa: E501
from swagger_server.models.api_response_qos import ApiResponseQos  # noqa: E501
from swagger_server.test import BaseTestCase


class TestQoSApiController(BaseTestCase):
    """QoSApiController integration test stubs"""

    def test_enable_delivery(self):
        """Test case for enable_delivery

        
        """
        body = True
        response = self.client.open(
            '/Marti/api/qos/delivery/enable',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_enable_dos(self):
        """Test case for enable_dos

        
        """
        body = True
        response = self.client.open(
            '/Marti/api/qos/dos/enable',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_enable_read(self):
        """Test case for enable_read

        
        """
        body = True
        response = self.client.open(
            '/Marti/api/qos/read/enable',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_active_delivery_rate_limit(self):
        """Test case for get_active_delivery_rate_limit

        
        """
        response = self.client.open(
            '/Marti/api/qos/ratelimit/delivery/active',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_active_dos_rate_limit(self):
        """Test case for get_active_dos_rate_limit

        
        """
        response = self.client.open(
            '/Marti/api/qos/ratelimit/dos/active',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_active_read_rate_limit(self):
        """Test case for get_active_read_rate_limit

        
        """
        response = self.client.open(
            '/Marti/api/qos/ratelimit/read/active',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_qos_conf(self):
        """Test case for get_qos_conf

        
        """
        response = self.client.open(
            '/Marti/api/qos/conf',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
