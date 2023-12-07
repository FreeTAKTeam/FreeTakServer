# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response_list_tak_cert import ApiResponseListTakCert  # noqa: E501
from swagger_server.models.api_response_tak_cert import ApiResponseTakCert  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCertManagerAdminApiController(BaseTestCase):
    """CertManagerAdminApiController integration test stubs"""

    def test_delete_certificates(self):
        """Test case for delete_certificates

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/delete/{ids}'.format(ids='ids_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_certificate(self):
        """Test case for download_certificate

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/{hash}/download'.format(hash='hash_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_download_certificates(self):
        """Test case for download_certificates

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/download/{ids}'.format(ids='ids_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_active(self):
        """Test case for get_active

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/active',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_all1(self):
        """Test case for get_all1

        
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '/Marti/api/certadmin/cert',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_certificate(self):
        """Test case for get_certificate

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/{hash}'.format(hash='hash_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_expired(self):
        """Test case for get_expired

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/expired',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_replaced(self):
        """Test case for get_replaced

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/replaced',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_revoked(self):
        """Test case for get_revoked

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/revoked',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_revoke_certificate(self):
        """Test case for revoke_certificate

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/{hash}'.format(hash='hash_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_revoke_certificates(self):
        """Test case for revoke_certificates

        
        """
        response = self.client.open(
            '/Marti/api/certadmin/cert/revoke/{ids}'.format(ids='ids_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
