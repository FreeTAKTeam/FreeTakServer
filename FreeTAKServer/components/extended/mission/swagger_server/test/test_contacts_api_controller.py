# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.remote_subscription import RemoteSubscription  # noqa: E501
from swagger_server.test import BaseTestCase


class TestContactsApiController(BaseTestCase):
    """ContactsApiController integration test stubs"""

    def test_get_all_contacts(self):
        """Test case for get_all_contacts

        
        """
        query_string = [('sort_by', 'CALLSIGN'),
                        ('direction', 'ASCENDING'),
                        ('no_federates', false)]
        response = self.client.open(
            '/Marti/api/contacts/all',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
