# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_citrap_body import ApiCitrapBody  # noqa: E501
from swagger_server.models.citrap_id_body import CitrapIdBody  # noqa: E501
from swagger_server.models.id_attachment_body import IdAttachmentBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCiTrapReportApiController(BaseTestCase):
    """CiTrapReportApiController integration test stubs"""

    def test_add_attachment(self):
        """Test case for add_attachment

        
        """
        body = IdAttachmentBody()
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/citrap/{id}/attachment'.format(id='id_example'),
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_report(self):
        """Test case for delete_report

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/citrap/{id}'.format(id='id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_report(self):
        """Test case for get_report

        
        """
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/citrap/{id}'.format(id='id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_report(self):
        """Test case for post_report

        
        """
        body = ApiCitrapBody()
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/citrap',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_put_report(self):
        """Test case for put_report

        
        """
        body = CitrapIdBody()
        query_string = [('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/citrap/{id}'.format(id='id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_reports(self):
        """Test case for search_reports

        
        """
        query_string = [('keywords', 'keywords_example'),
                        ('bbox', 'bbox_example'),
                        ('start_time', 'start_time_example'),
                        ('end_time', 'end_time_example'),
                        ('max_report_count', 'max_report_count_example'),
                        ('type', 'type_example'),
                        ('callsign', 'callsign_example'),
                        ('subscribe', 'subscribe_example'),
                        ('client_uid', 'client_uid_example')]
        response = self.client.open(
            '/Marti/api/citrap',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
