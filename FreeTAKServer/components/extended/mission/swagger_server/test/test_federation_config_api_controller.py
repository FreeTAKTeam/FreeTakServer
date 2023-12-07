# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_federation_config_info import ApiResponseFederationConfigInfo  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.federation_config_info import FederationConfigInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFederationConfigApiController(BaseTestCase):
    """FederationConfigApiController integration test stubs"""

    def test_get_federation_config(self):
        """Test case for get_federation_config

        
        """
        response = self.client.open(
            '/Marti/api/federationconfig',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_federation_config(self):
        """Test case for modify_federation_config

        
        """
        body = FederationConfigInfo()
        response = self.client.open(
            '/Marti/api/federationconfig',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_verify_federation_truststore(self):
        """Test case for verify_federation_truststore

        
        """
        response = self.client.open(
            '/Marti/api/federationconfig/verify',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
