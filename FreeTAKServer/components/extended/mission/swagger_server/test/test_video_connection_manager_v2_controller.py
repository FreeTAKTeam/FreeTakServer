# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.video_collections import VideoCollections  # noqa: E501
from swagger_server.models.video_connection import VideoConnection  # noqa: E501
from swagger_server.test import BaseTestCase


class TestVideoConnectionManagerV2Controller(BaseTestCase):
    """VideoConnectionManagerV2Controller integration test stubs"""

    def test_create_video_connection(self):
        """Test case for create_video_connection

        
        """
        body = VideoCollections()
        response = self.client.open(
            '/Marti/api/video',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_video_connection(self):
        """Test case for delete_video_connection

        
        """
        response = self.client.open(
            '/Marti/api/video/{uid}'.format(uid='uid_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_video_collections(self):
        """Test case for get_video_collections

        
        """
        query_string = [('protocol', 'protocol_example')]
        response = self.client.open(
            '/Marti/api/video',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_video_connection(self):
        """Test case for get_video_connection

        
        """
        response = self.client.open(
            '/Marti/api/video/{uid}'.format(uid='uid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_video_connection(self):
        """Test case for update_video_connection

        
        """
        body = VideoConnection()
        response = self.client.open(
            '/Marti/api/video/{uid}'.format(uid='uid_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
