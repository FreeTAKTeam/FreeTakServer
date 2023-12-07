# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_list_cot_search import ApiResponseListCotSearch  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCotQueryApiController(BaseTestCase):
    """CotQueryApiController integration test stubs"""

    def test_get_all_searches(self):
        """Test case for get_all_searches

        
        """
        response = self.client.open(
            '/Marti/api',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_date(self):
        """Test case for get_date

        
        """
        response = self.client.open(
            '/Marti/api/cot/search/date',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_search(self):
        """Test case for get_search

        
        """
        response = self.client.open(
            '/Marti/api/cot/search/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
