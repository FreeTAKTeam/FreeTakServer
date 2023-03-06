# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_iconset_body import ApiIconsetBody  # noqa: E501
from swagger_server.models.api_response_list_string import ApiResponseListString  # noqa: E501
from swagger_server.models.api_response_set_string import ApiResponseSetString  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.test import BaseTestCase


class TestIconsetIconApiController(BaseTestCase):
    """IconsetIconApiController integration test stubs"""

    def test_get_all_icon_urls_for_iconset(self):
        """Test case for get_all_icon_urls_for_iconset

        
        """
        response = self.client.open(
            '/Marti/api/iconseturl/{uid}'.format(uid='uid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all_iconset_uids(self):
        """Test case for get_all_iconset_uids

        
        """
        response = self.client.open(
            '/Marti/api/iconset/all/uid',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_icon(self):
        """Test case for get_icon

        
        """
        response = self.client.open(
            '/Marti/api/icon/{uid}/{group}/{name}'.format(uid='uid_example', group='group_example', name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_icon_image(self):
        """Test case for get_icon_image

        
        """
        query_string = [('iconsetpath', 'iconsetpath_example'),
                        ('cot_type', 'cot_type_example'),
                        ('medevac', true),
                        ('group_name', 'group_name_example'),
                        ('role', 'role_example'),
                        ('color', 789),
                        ('relative', true)]
        response = self.client.open(
            '/Marti/api/iconimage',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_icon_url(self):
        """Test case for get_icon_url

        
        """
        query_string = [('iconsetpath', 'iconsetpath_example'),
                        ('cot_type', 'cot_type_example'),
                        ('medevac', true),
                        ('group_name', 'group_name_example'),
                        ('role', 'role_example'),
                        ('color', 789),
                        ('relative', true)]
        response = self.client.open(
            '/Marti/api/iconurl',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_iconset_zip(self):
        """Test case for post_iconset_zip

        
        """
        body = ApiIconsetBody()
        response = self.client.open(
            '/Marti/api/iconset',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
