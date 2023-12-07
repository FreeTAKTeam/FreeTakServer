# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.name_submit_body import NameSubmitBody  # noqa: E501
from swagger_server.models.name_submit_body1 import NameSubmitBody1  # noqa: E501
from swagger_server.models.submit_result_body import SubmitResultBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPluginDataApiController(BaseTestCase):
    """PluginDataApiController integration test stubs"""

    def test_delete_from_plugin(self):
        """Test case for delete_from_plugin

        
        """
        query_string = [('all_request_params', {'key': 'all_request_params_example'})]
        response = self.client.open(
            '/Marti/api/plugins/{name}/submit'.format(name='name_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_request_from_plugin(self):
        """Test case for request_from_plugin

        
        """
        query_string = [('all_request_params', {'key': 'all_request_params_example'})]
        response = self.client.open(
            '/Marti/api/plugins/{name}/submit'.format(name='name_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_submit_to_plugin_utf8(self):
        """Test case for submit_to_plugin_utf8

        
        """
        body = NameSubmitBody()
        query_string = [('all_request_params', {'key': 'all_request_params_example'})]
        response = self.client.open(
            '/Marti/api/plugins/{name}/submit'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_submit_to_plugin_utf8_with_result(self):
        """Test case for submit_to_plugin_utf8_with_result

        
        """
        body = SubmitResultBody()
        query_string = [('all_request_params', {'key': 'all_request_params_example'})]
        response = self.client.open(
            '/Marti/api/plugins/{name}/submit/result'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_in_plugin(self):
        """Test case for update_in_plugin

        
        """
        body = NameSubmitBody1()
        query_string = [('all_request_params', {'key': 'all_request_params_example'})]
        response = self.client.open(
            '/Marti/api/plugins/{name}/submit'.format(name='name_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
