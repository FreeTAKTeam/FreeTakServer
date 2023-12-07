# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_connection_modify_result import ApiResponseConnectionModifyResult  # noqa: E501
from swagger_server.models.api_response_data_feed import ApiResponseDataFeed  # noqa: E501
from swagger_server.models.api_response_input import ApiResponseInput  # noqa: E501
from swagger_server.models.api_response_input_metric import ApiResponseInputMetric  # noqa: E501
from swagger_server.models.api_response_list_data_feed import ApiResponseListDataFeed  # noqa: E501
from swagger_server.models.api_response_map_string_integer import ApiResponseMapStringInteger  # noqa: E501
from swagger_server.models.api_response_messaging_config_info import ApiResponseMessagingConfigInfo  # noqa: E501
from swagger_server.models.api_response_sorted_set_input_metric import ApiResponseSortedSetInputMetric  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.data_feed import DataFeed  # noqa: E501
from swagger_server.models.input import Input  # noqa: E501
from swagger_server.models.messaging_config_info import MessagingConfigInfo  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSubmissionApiController(BaseTestCase):
    """SubmissionApiController integration test stubs"""

    def test_create_data_feed(self):
        """Test case for create_data_feed

        
        """
        body = DataFeed()
        response = self.client.open(
            '/Marti/api/datafeeds',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_input(self):
        """Test case for create_input

        
        """
        body = Input()
        response = self.client.open(
            '/Marti/api/inputs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_data_feed(self):
        """Test case for delete_data_feed

        
        """
        response = self.client.open(
            '/Marti/api/datafeeds/{name}'.format(name='name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_input(self):
        """Test case for delete_input

        
        """
        response = self.client.open(
            '/Marti/api/inputs/{name}'.format(name='name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_disable_store_forward_chat(self):
        """Test case for disable_store_forward_chat

        
        """
        response = self.client.open(
            '/Marti/api/inputs/storeForwardChat/disable',
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_enable_store_forward_chat(self):
        """Test case for enable_store_forward_chat

        
        """
        response = self.client.open(
            '/Marti/api/inputs/storeForwardChat/enable',
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_config_info(self):
        """Test case for get_config_info

        
        """
        response = self.client.open(
            '/Marti/api/inputs/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_feed(self):
        """Test case for get_data_feed

        
        """
        response = self.client.open(
            '/Marti/api/datafeeds/{name}'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_feeds(self):
        """Test case for get_data_feeds

        
        """
        response = self.client.open(
            '/Marti/api/datafeeds',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_database_cot_counts(self):
        """Test case for get_database_cot_counts

        
        """
        response = self.client.open(
            '/Marti/api/database/cotCount',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_input_metric(self):
        """Test case for get_input_metric

        
        """
        response = self.client.open(
            '/Marti/api/inputs/{name}'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_input_metrics(self):
        """Test case for get_input_metrics

        
        """
        query_string = [('exclude_data_feeds', false)]
        response = self.client.open(
            '/Marti/api/inputs',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_is_store_forward_chat_enabled(self):
        """Test case for is_store_forward_chat_enabled

        
        """
        response = self.client.open(
            '/Marti/api/inputs/storeForwardChat/enabled',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_config_info(self):
        """Test case for modify_config_info

        
        """
        body = MessagingConfigInfo()
        response = self.client.open(
            '/Marti/api/inputs/config',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_data_feed(self):
        """Test case for modify_data_feed

        
        """
        body = DataFeed()
        response = self.client.open(
            '/Marti/api/datafeeds/{name}'.format(name='name_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_modify_input(self):
        """Test case for modify_input

        
        """
        body = Input()
        response = self.client.open(
            '/Marti/api/inputs/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
