# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_list_client_endpoint import ApiResponseListClientEndpoint  # noqa: E501
from swagger_server.test import BaseTestCase


class TestContactManagerApiController(BaseTestCase):
    """ContactManagerApiController integration test stubs"""

    def test_get_client_endpoints(self):
        """Test case for get_client_endpoints

        
        """
        query_string = [('sec_ago', 0),
                        ('show_currently_connected_clients', 'false'),
                        ('show_most_recent_only', 'false')]
        response = self.client.open(
            '/Marti/api/clientEndPoints',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
