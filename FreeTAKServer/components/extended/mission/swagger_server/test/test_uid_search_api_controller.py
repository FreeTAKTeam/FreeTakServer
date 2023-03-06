# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_list_uid_result import ApiResponseListUIDResult  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUidSearchApiController(BaseTestCase):
    """UidSearchApiController integration test stubs"""

    def test_get_uid_results(self):
        """Test case for get_uid_results

        
        """
        query_string = [('start_date', 'start_date_example'),
                        ('end_date', 'end_date_example')]
        response = self.client.open(
            '/Marti/api/uidsearch',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
