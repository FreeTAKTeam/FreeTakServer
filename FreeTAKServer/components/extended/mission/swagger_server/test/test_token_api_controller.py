# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_list_token_result import ApiResponseListTokenResult  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTokenApiController(BaseTestCase):
    """TokenApiController integration test stubs"""

    def test_get_all(self):
        """Test case for get_all

        
        """
        query_string = [('expired', false)]
        response = self.client.open(
            '/Marti/api/token',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_revoke_token(self):
        """Test case for revoke_token

        
        """
        response = self.client.open(
            '/Marti/api/token/{token}'.format(token='token_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_revoke_tokens(self):
        """Test case for revoke_tokens

        
        """
        response = self.client.open(
            '/Marti/api/token/revoke/{tokens}'.format(tokens='tokens_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
