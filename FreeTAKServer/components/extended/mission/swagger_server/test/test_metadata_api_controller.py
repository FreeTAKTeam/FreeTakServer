# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestMetadataApiController(BaseTestCase):
    """MetadataApiController integration test stubs"""

    def test_set_expiration(self):
        """Test case for set_expiration

        
        """
        query_string = [('expiration', 789)]
        response = self.client.open(
            '/Marti/api/sync/metadata/{hash}/expiration'.format(hash='hash_example'),
            method='PUT',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_metadata(self):
        """Test case for set_metadata

        
        """
        body = 'body_example'
        response = self.client.open(
            '/Marti/api/sync/metadata/{hash}/{metadata}'.format(hash='hash_example', metadata='metadata_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_metadata_keywords(self):
        """Test case for set_metadata_keywords

        
        """
        body = ['body_example']
        response = self.client.open(
            '/Marti/api/sync/metadata/{hash}/keywords'.format(hash='hash_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
