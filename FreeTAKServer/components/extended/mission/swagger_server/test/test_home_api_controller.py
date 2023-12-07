# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestHomeApiController(BaseTestCase):
    """HomeApiController integration test stubs"""

    def test_get_home(self):
        """Test case for get_home

        
        """
        response = self.client.open(
            '/Marti/api/home',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user_roles(self):
        """Test case for get_user_roles

        
        """
        response = self.client.open(
            '/Marti/api/util/user/roles',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_ver(self):
        """Test case for get_ver

        
        """
        response = self.client.open(
            '/Marti/api/ver',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_is_admin(self):
        """Test case for is_admin

        
        """
        response = self.client.open(
            '/Marti/api/util/isAdmin',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
