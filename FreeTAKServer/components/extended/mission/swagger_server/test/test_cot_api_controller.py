# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestCotApiController(BaseTestCase):
    """CotApiController integration test stubs"""

    def test_get_all_cot_events(self):
        """Test case for get_all_cot_events

        
        """
        query_string = [('secago', 789),
                        ('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00')]
        response = self.client.open(
            '/Marti/api/cot/xml/{uid}/all'.format(uid='uid_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cot_event(self):
        """Test case for get_cot_event

        
        """
        response = self.client.open(
            '/Marti/api/cot/xml/{uid}'.format(uid='uid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cot_events(self):
        """Test case for get_cot_events

        
        """
        query_string = [('uids', 'uids_example')]
        response = self.client.open(
            '/Marti/api/cot',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_cot_events_by_time_and_bbox(self):
        """Test case for get_cot_events_by_time_and_bbox

        
        """
        query_string = [('start', '2013-10-20T19:20:30+01:00'),
                        ('end', '2013-10-20T19:20:30+01:00'),
                        ('left', 1.2),
                        ('bottom', 1.2),
                        ('right', 1.2),
                        ('top', 1.2)]
        response = self.client.open(
            '/Marti/api/cot/sa',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
