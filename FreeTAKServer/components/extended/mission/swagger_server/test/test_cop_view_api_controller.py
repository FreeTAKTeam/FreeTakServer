# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_list_mission import ApiResponseListMission  # noqa: E501
from swagger_server.models.api_response_set_cop_hierarchy_node import ApiResponseSetCopHierarchyNode  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCopViewApiController(BaseTestCase):
    """CopViewApiController integration test stubs"""

    def test_get_all_cop_missions(self):
        """Test case for get_all_cop_missions

        
        """
        query_string = [('path', 'path_example'),
                        ('offset', 56),
                        ('size', 56)]
        response = self.client.open(
            '/Marti/api/cops',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_hierarchy(self):
        """Test case for get_hierarchy

        
        """
        response = self.client.open(
            '/Marti/api/cops/hierarchy',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
