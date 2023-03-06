# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_caveat import ApiResponseCaveat  # noqa: E501
from swagger_server.models.api_response_classification import ApiResponseClassification  # noqa: E501
from swagger_server.models.api_response_list_caveat import ApiResponseListCaveat  # noqa: E501
from swagger_server.models.api_response_list_classification import ApiResponseListClassification  # noqa: E501
from swagger_server.models.api_response_long import ApiResponseLong  # noqa: E501
from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server.test import BaseTestCase


class TestClassificationApiController(BaseTestCase):
    """ClassificationApiController integration test stubs"""

    def test_delete_caveat(self):
        """Test case for delete_caveat

        
        """
        response = self.client.open(
            '/Marti/api/caveat/{name}'.format(name='name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_classification(self):
        """Test case for delete_classification

        
        """
        response = self.client.open(
            '/Marti/api/classification/{level}'.format(level='level_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_caveat(self):
        """Test case for get_all_caveat

        
        """
        response = self.client.open(
            '/Marti/api/caveat',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_classifications(self):
        """Test case for get_all_classifications

        
        """
        response = self.client.open(
            '/Marti/api/classification',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_classification_for_level(self):
        """Test case for get_classification_for_level

        
        """
        response = self.client.open(
            '/Marti/api/classification/{level}'.format(level='level_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_new_caveat(self):
        """Test case for new_caveat

        
        """
        response = self.client.open(
            '/Marti/api/caveat/{name}'.format(name='name_example'),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_new_classification(self):
        """Test case for new_classification

        
        """
        response = self.client.open(
            '/Marti/api/classification/{level}'.format(level='level_example'),
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_caveats_for_classification(self):
        """Test case for set_caveats_for_classification

        
        """
        body = Classification()
        response = self.client.open(
            '/Marti/api/classification',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
