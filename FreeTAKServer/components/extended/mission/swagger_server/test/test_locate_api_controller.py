# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestLocateApiController(BaseTestCase):
    """LocateApiController integration test stubs"""

    def test_locate(self):
        """Test case for locate

        
        """
        query_string = [('latitude', 1.2),
                        ('longitude', 1.2),
                        ('name', 'name_example'),
                        ('remarks', 'remarks_example')]
        response = self.client.open(
            '/locate/api',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
