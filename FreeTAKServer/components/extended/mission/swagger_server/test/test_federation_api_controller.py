# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_federatecertificates_body import ApiFederatecertificatesBody  # noqa: E501
from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_connection_status import ApiResponseConnectionStatus  # noqa: E501
from swagger_server.models.api_response_federate import ApiResponseFederate  # noqa: E501
from swagger_server.models.api_response_federation_outgoing import ApiResponseFederationOutgoing  # noqa: E501
from swagger_server.models.api_response_list_certificate_summary import ApiResponseListCertificateSummary  # noqa: E501
from swagger_server.models.api_response_list_connection_info_summary import ApiResponseListConnectionInfoSummary  # noqa: E501
from swagger_server.models.api_response_list_federate_ca_group_association import ApiResponseListFederateCAGroupAssociation  # noqa: E501
from swagger_server.models.api_response_list_federate_group_association import ApiResponseListFederateGroupAssociation  # noqa: E501
from swagger_server.models.api_response_list_string import ApiResponseListString  # noqa: E501
from swagger_server.models.api_response_map_string_string import ApiResponseMapStringString  # noqa: E501
from swagger_server.models.api_response_sorted_set_federate import ApiResponseSortedSetFederate  # noqa: E501
from swagger_server.models.api_response_sorted_set_outgoing_connection_summary import ApiResponseSortedSetOutgoingConnectionSummary  # noqa: E501
from swagger_server.models.api_response_sorted_set_remote_contact import ApiResponseSortedSetRemoteContact  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.federate import Federate  # noqa: E501
from swagger_server.models.federate_ca_group_association import FederateCAGroupAssociation  # noqa: E501
from swagger_server.models.federate_group_association import FederateGroupAssociation  # noqa: E501
from swagger_server.models.federation_outgoing import FederationOutgoing  # noqa: E501
from swagger_server.test import BaseTestCase


class TestFederationApiController(BaseTestCase):
    """FederationApiController integration test stubs"""

    def test_add_federate_ca_group(self):
        """Test case for add_federate_ca_group

        
        """
        body = FederateCAGroupAssociation()
        response = self.client.open(
            '/Marti/api/federatecagroups',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_federate_group(self):
        """Test case for add_federate_group

        
        """
        body = FederateGroupAssociation()
        response = self.client.open(
            '/Marti/api/federategroups',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_federate_group_map(self):
        """Test case for add_federate_group_map

        
        """
        query_string = [('remote_group', 'remote_group_example'),
                        ('local_group', 'local_group_example')]
        response = self.client.open(
            '/Marti/api/federategroupsmap/{federateId}'.format(federate_id='federate_id_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_change_connection_status(self):
        """Test case for change_connection_status

        
        """
        query_string = [('new_status', true)]
        response = self.client.open(
            '/Marti/api/outgoingconnectionstatus/{name}'.format(name='name_example'),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_clear_disruption_data(self):
        """Test case for clear_disruption_data

        
        """
        response = self.client.open(
            '/Marti/api/clearFederationEvents',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_outgoing_connection(self):
        """Test case for create_outgoing_connection

        
        """
        body = FederationOutgoing()
        response = self.client.open(
            '/Marti/api/outgoingconnections',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_federate(self):
        """Test case for delete_federate

        
        """
        response = self.client.open(
            '/Marti/api/federatedetails/{federateId}'.format(federate_id='federate_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_federate_certificate_ca(self):
        """Test case for delete_federate_certificate_ca

        
        """
        response = self.client.open(
            '/Marti/api/federatecertificates/{fingerprint}'.format(fingerprint='fingerprint_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_outgoing_connection(self):
        """Test case for delete_outgoing_connection

        
        """
        response = self.client.open(
            '/Marti/api/outgoingconnections/{name}'.format(name='name_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_active_connections(self):
        """Test case for get_active_connections

        
        """
        response = self.client.open(
            '/Marti/api/activeconnections',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_connection_status(self):
        """Test case for get_connection_status

        
        """
        response = self.client.open(
            '/Marti/api/outgoingconnectionstatus/{name}'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federate_ca_groups(self):
        """Test case for get_federate_ca_groups

        
        """
        response = self.client.open(
            '/Marti/api/federatecagroups/{caId}'.format(ca_id='ca_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federate_certificates(self):
        """Test case for get_federate_certificates

        
        """
        response = self.client.open(
            '/Marti/api/federatecertificates',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federate_contacts(self):
        """Test case for get_federate_contacts

        
        """
        response = self.client.open(
            '/Marti/api/federatecontacts/{federateId}'.format(federate_id='federate_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federate_details(self):
        """Test case for get_federate_details

        
        """
        response = self.client.open(
            '/Marti/api/federatedetails/{id}'.format(id='id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federate_groups(self):
        """Test case for get_federate_groups

        
        """
        response = self.client.open(
            '/Marti/api/federategroups/{federateId}'.format(federate_id='federate_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federate_groups_map(self):
        """Test case for get_federate_groups_map

        
        """
        response = self.client.open(
            '/Marti/api/federategroupsmap/{federateId}'.format(federate_id='federate_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federate_remote_groups(self):
        """Test case for get_federate_remote_groups

        
        """
        response = self.client.open(
            '/Marti/api/federateremotegroups/{federateId}'.format(federate_id='federate_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_federates(self):
        """Test case for get_federates

        
        """
        response = self.client.open(
            '/Marti/api/federates',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_num(self):
        """Test case for get_num

        
        """
        response = self.client.open(
            '/Marti/api/fednum',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_outgoing_connection(self):
        """Test case for get_outgoing_connection

        
        """
        response = self.client.open(
            '/Marti/api/outgoingconnections/{name}'.format(name='name_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_outgoing_connections(self):
        """Test case for get_outgoing_connections

        
        """
        response = self.client.open(
            '/Marti/api/outgoingconnections',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_federate_ca_group(self):
        """Test case for remove_federate_ca_group

        
        """
        query_string = [('group', 'group_example'),
                        ('direction', 'direction_example')]
        response = self.client.open(
            '/Marti/api/federatecagroups/{caId}'.format(ca_id='ca_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_federate_group(self):
        """Test case for remove_federate_group

        
        """
        query_string = [('group', 'group_example'),
                        ('direction', 'direction_example')]
        response = self.client.open(
            '/Marti/api/federategroups/{federateId}'.format(federate_id='federate_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove_federate_group_map(self):
        """Test case for remove_federate_group_map

        
        """
        query_string = [('remote_group', 'remote_group_example'),
                        ('local_group', 'local_group_example')]
        response = self.client.open(
            '/Marti/api/federategroupsmap/{federateId}'.format(federate_id='federate_id_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_save_federate_certificate_ca(self):
        """Test case for save_federate_certificate_ca

        
        """
        body = ApiFederatecertificatesBody()
        response = self.client.open(
            '/Marti/api/federatecertificates',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_save_federate_group_configuration(self):
        """Test case for save_federate_group_configuration

        
        """
        response = self.client.open(
            '/Marti/api/federategroupconfig',
            method='POST')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_federate_details(self):
        """Test case for update_federate_details

        
        """
        body = Federate()
        response = self.client.open(
            '/Marti/api/federatedetails',
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
