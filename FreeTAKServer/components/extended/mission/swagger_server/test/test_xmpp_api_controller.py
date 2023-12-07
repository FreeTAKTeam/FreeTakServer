# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.uid_filename_body import UidFilenameBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestXmppApiController(BaseTestCase):
    """XmppApiController integration test stubs"""

    def test_get_file(self):
        """Test case for get_file

        
        """
        response = self.client.open(
            '/Marti/api/xmpp/transfer/{uid}/{filename}'.format(uid='uid_example', filename='filename_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_file(self):
        """Test case for put_file

        
        """
        body = UidFilenameBody()
        response = self.client.open(
            '/Marti/api/xmpp/transfer/{uid}/{filename}'.format(uid='uid_example', filename='filename_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
