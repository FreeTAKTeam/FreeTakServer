# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.tak_user import TAKUser  # noqa: E501
from swagger_server.test import BaseTestCase


class TestRegistrationApiController(BaseTestCase):
    """RegistrationApiController integration test stubs"""

    def test_confirm(self):
        """Test case for confirm

        
        """
        response = self.client.open(
            '/register/token/{token}'.format(token='token_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_users1(self):
        """Test case for get_all_users1

        
        """
        response = self.client.open(
            '/register/admin/users',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_invite(self):
        """Test case for invite

        
        """
        query_string = [('email_address', 'email_address_example'),
                        ('group', '[\"__ANON__\"]')]
        response = self.client.open(
            '/register/admin/invite',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_sign_up(self):
        """Test case for sign_up

        
        """
        query_string = [('email_address', 'email_address_example'),
                        ('token', 'token_example')]
        response = self.client.open(
            '/register/user',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
