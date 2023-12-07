# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_collection_map_layer import ApiResponseCollectionMapLayer  # noqa: E501
from swagger_server.models.api_response_map_layer import ApiResponseMapLayer  # noqa: E501
from swagger_server.models.map_layer import MapLayer  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMapLayersApiController(BaseTestCase):
    """MapLayersApiController integration test stubs"""

    def test_create_map_layer1(self):
        """Test case for create_map_layer1

        
        """
        body = MapLayer()
        response = self.client.open(
            '/Marti/api/maplayers',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_map_layer1(self):
        """Test case for delete_map_layer1

        
        """
        response = self.client.open(
            '/Marti/api/maplayers/{uid}'.format(uid='uid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_map_layers(self):
        """Test case for get_all_map_layers

        
        """
        response = self.client.open(
            '/Marti/api/maplayers/all',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_map_layer_for_uid(self):
        """Test case for get_map_layer_for_uid

        
        """
        response = self.client.open(
            '/Marti/api/maplayers/{uid}'.format(uid='uid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_map_layer1(self):
        """Test case for update_map_layer1

        
        """
        body = MapLayer()
        response = self.client.open(
            '/Marti/api/maplayers',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
