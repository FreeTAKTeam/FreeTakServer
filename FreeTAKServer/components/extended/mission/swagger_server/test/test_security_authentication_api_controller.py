# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_authentication_config_info import ApiResponseAuthenticationConfigInfo  # noqa: E501
from swagger_server.models.api_response_security_config_info import ApiResponseSecurityConfigInfo  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.authentication_config_info import AuthenticationConfigInfo  # noqa: E501
from swagger_server.models.security_config_info import SecurityConfigInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSecurityAuthenticationApiController(BaseTestCase):
    """SecurityAuthenticationApiController integration test stubs"""

    def test_get_auth_config(self):
        """Test case for get_auth_config

        
        """
        response = self.client.open(
            '/Marti/api/authentication/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_sec_config(self):
        """Test case for get_sec_config

        
        """
        response = self.client.open(
            '/Marti/api/security/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_is_secure(self):
        """Test case for is_secure

        
        """
        response = self.client.open(
            '/Marti/api/security/isSecure',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_auth_config(self):
        """Test case for modify_auth_config

        
        """
        body = AuthenticationConfigInfo()
        response = self.client.open(
            '/Marti/api/authentication/config',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_sec_config(self):
        """Test case for modify_sec_config

        
        """
        body = SecurityConfigInfo()
        response = self.client.open(
            '/Marti/api/security/config',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_test_auth_config(self):
        """Test case for test_auth_config

        
        """
        response = self.client.open(
            '/Marti/api/authentication/config',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_verify_config(self):
        """Test case for verify_config

        
        """
        response = self.client.open(
            '/Marti/api/security/verifyConfig',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
