# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.vbm_configuration_model import VBMConfigurationModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestVbmConfigurationApiController(BaseTestCase):
    """VbmConfigurationApiController integration test stubs"""

    def test_get_vbm_configuration(self):
        """Test case for get_vbm_configuration

        
        """
        response = self.client.open(
            '/vbm/api/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_vbm_configuration(self):
        """Test case for set_vbm_configuration

        
        """
        body = VBMConfigurationModel()
        response = self.client.open(
            '/vbm/api/config',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
