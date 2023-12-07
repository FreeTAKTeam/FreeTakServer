# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_integer import ApiResponseInteger  # noqa: E501
from swagger_server.models.api_response_list_repeatable import ApiResponseListRepeatable  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRepeaterApiController(BaseTestCase):
    """RepeaterApiController integration test stubs"""

    def test_get_list(self):
        """Test case for get_list

        
        """
        response = self.client.open(
            '/Marti/api/repeater/list',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_period(self):
        """Test case for get_period

        
        """
        response = self.client.open(
            '/Marti/api/repeater/period',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove(self):
        """Test case for remove

        
        """
        response = self.client.open(
            '/Marti/api/repeater/remove/{uid}'.format(uid='uid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_period(self):
        """Test case for set_period

        
        """
        body = 56
        response = self.client.open(
            '/Marti/api/repeater/period',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
