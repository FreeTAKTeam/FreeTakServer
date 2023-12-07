# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestSequenceApiController(BaseTestCase):
    """SequenceApiController integration test stubs"""

    def test_get_next_in_sequence(self):
        """Test case for get_next_in_sequence

        
        """
        response = self.client.open(
            '/Marti/api/sync/sequence/{key}'.format(key='key_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
