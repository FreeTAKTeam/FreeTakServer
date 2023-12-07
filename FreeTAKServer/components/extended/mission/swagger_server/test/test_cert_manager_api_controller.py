# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestCertManagerApiController(BaseTestCase):
    """CertManagerApiController integration test stubs"""

    def test_get_config(self):
        """Test case for get_config

        
        """
        response = self.client.open(
            '/Marti/api/tls/config',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_make_key_store(self):
        """Test case for make_key_store

        
        """
        query_string = [('cn', 'cn_example'),
                        ('password', 'atakatak')]
        response = self.client.open(
            '/Marti/api/tls/makeClientKeyStore',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_sign_client_cert(self):
        """Test case for sign_client_cert

        
        """
        body = 'body_example'
        query_string = [('client_uid', ''),
                        ('version', 'version_example')]
        response = self.client.open(
            '/Marti/api/tls/signClient',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_sign_client_cert_v2(self):
        """Test case for sign_client_cert_v2

        
        """
        body = 'body_example'
        query_string = [('client_uid', ''),
                        ('version', 'version_example')]
        response = self.client.open(
            '/Marti/api/tls/signClient/v2',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
