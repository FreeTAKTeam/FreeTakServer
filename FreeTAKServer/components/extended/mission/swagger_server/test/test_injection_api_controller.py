# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_collection_injector_config import ApiResponseCollectionInjectorConfig  # noqa: E501
from swagger_server.models.api_response_set_injector_config import ApiResponseSetInjectorConfig  # noqa: E501
from swagger_server.models.injector_config import InjectorConfig  # noqa: E501
from swagger_server.test import BaseTestCase


class TestInjectionApiController(BaseTestCase):
    """InjectionApiController integration test stubs"""

    def test_delete_injector(self):
        """Test case for delete_injector

        
        """
        query_string = [('uid', 'uid_example'),
                        ('to_inject', 'to_inject_example')]
        response = self.client.open(
            '/Marti/api/injectors/cot/uid',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_cot_injectors(self):
        """Test case for get_all_cot_injectors

        
        """
        response = self.client.open(
            '/Marti/api/injectors/cot/uid',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_one_cot_injector(self):
        """Test case for get_one_cot_injector

        
        """
        response = self.client.open(
            '/Marti/api/injectors/cot/uid/{uid}'.format(uid='uid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_cot_injector(self):
        """Test case for put_cot_injector

        
        """
        body = InjectorConfig()
        response = self.client.open(
            '/Marti/api/injectors/cot/uid',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
