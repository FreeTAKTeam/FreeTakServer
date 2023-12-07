# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_collection_string import ApiResponseCollectionString  # noqa: E501
from swagger_server.models.api_response_entry_string_string import ApiResponseEntryStringString  # noqa: E501
from swagger_server.models.api_response_map_string_collection_string import ApiResponseMapStringCollectionString  # noqa: E501
from swagger_server.models.properties_uid_body import PropertiesUidBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPropertiesApiController(BaseTestCase):
    """PropertiesApiController integration test stubs"""

    def test_clear_all_property(self):
        """Test case for clear_all_property

        
        """
        response = self.client.open(
            '/Marti/api/properties/{uid}/all'.format(uid='uid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_clear_property(self):
        """Test case for clear_property

        
        """
        response = self.client.open(
            '/Marti/api/properties/{uid}/{key}'.format(uid='uid_example', key='key_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_property_for_uid(self):
        """Test case for get_all_property_for_uid

        
        """
        response = self.client.open(
            '/Marti/api/properties/{uid}/all'.format(uid='uid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_property_keys(self):
        """Test case for get_all_property_keys

        
        """
        response = self.client.open(
            '/Marti/api/properties/uids',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_property_for_uid(self):
        """Test case for get_property_for_uid

        
        """
        response = self.client.open(
            '/Marti/api/properties/{uid}/{key}'.format(uid='uid_example', key='key_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_store_property(self):
        """Test case for store_property

        
        """
        body = PropertiesUidBody()
        response = self.client.open(
            '/Marti/api/properties/{uid}'.format(uid='uid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
