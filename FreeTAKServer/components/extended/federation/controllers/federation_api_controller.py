import connexion
import six

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
from swagger_server import util


def add_federate_ca_group(body):  # noqa: E501
    """add_federate_ca_group

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = FederateCAGroupAssociation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_federate_group(body):  # noqa: E501
    """add_federate_group

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = FederateGroupAssociation.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_federate_group_map(federate_id, remote_group, local_group):  # noqa: E501
    """add_federate_group_map

     # noqa: E501

    :param federate_id: 
    :type federate_id: str
    :param remote_group: 
    :type remote_group: str
    :param local_group: 
    :type local_group: str

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def change_connection_status(name, new_status):  # noqa: E501
    """change_connection_status

     # noqa: E501

    :param name: 
    :type name: str
    :param new_status: 
    :type new_status: bool

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def clear_disruption_data():  # noqa: E501
    """clear_disruption_data

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def create_outgoing_connection(body):  # noqa: E501
    """create_outgoing_connection

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseFederationOutgoing
    """
    if connexion.request.is_json:
        body = FederationOutgoing.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_federate(federate_id):  # noqa: E501
    """delete_federate

     # noqa: E501

    :param federate_id: 
    :type federate_id: str

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def delete_federate_certificate_ca(fingerprint):  # noqa: E501
    """delete_federate_certificate_ca

     # noqa: E501

    :param fingerprint: 
    :type fingerprint: str

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def delete_outgoing_connection(name):  # noqa: E501
    """delete_outgoing_connection

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def get_active_connections():  # noqa: E501
    """get_active_connections

     # noqa: E501


    :rtype: ApiResponseListConnectionInfoSummary
    """
    return 'do some magic!'


def get_connection_status(name):  # noqa: E501
    """get_connection_status

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseConnectionStatus
    """
    return 'do some magic!'


def get_federate_ca_groups(ca_id):  # noqa: E501
    """get_federate_ca_groups

     # noqa: E501

    :param ca_id: 
    :type ca_id: str

    :rtype: ApiResponseListFederateCAGroupAssociation
    """
    return 'do some magic!'


def get_federate_certificates():  # noqa: E501
    """get_federate_certificates

     # noqa: E501


    :rtype: ApiResponseListCertificateSummary
    """
    return 'do some magic!'


def get_federate_contacts(federate_id):  # noqa: E501
    """get_federate_contacts

     # noqa: E501

    :param federate_id: 
    :type federate_id: str

    :rtype: ApiResponseSortedSetRemoteContact
    """
    return 'do some magic!'


def get_federate_details(id):  # noqa: E501
    """get_federate_details

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiResponseFederate
    """
    return 'do some magic!'


def get_federate_groups(federate_id):  # noqa: E501
    """get_federate_groups

     # noqa: E501

    :param federate_id: 
    :type federate_id: str

    :rtype: ApiResponseListFederateGroupAssociation
    """
    return 'do some magic!'


def get_federate_groups_map(federate_id):  # noqa: E501
    """get_federate_groups_map

     # noqa: E501

    :param federate_id: 
    :type federate_id: str

    :rtype: ApiResponseMapStringString
    """
    return 'do some magic!'


def get_federate_remote_groups(federate_id):  # noqa: E501
    """get_federate_remote_groups

     # noqa: E501

    :param federate_id: 
    :type federate_id: str

    :rtype: ApiResponseListString
    """
    return 'do some magic!'


def get_federates():  # noqa: E501
    """get_federates

     # noqa: E501


    :rtype: ApiResponseSortedSetFederate
    """
    return 'do some magic!'


def get_num():  # noqa: E501
    """get_num

     # noqa: E501


    :rtype: int
    """
    return 'do some magic!'


def get_outgoing_connection(name):  # noqa: E501
    """get_outgoing_connection

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseFederationOutgoing
    """
    return 'do some magic!'


def get_outgoing_connections():  # noqa: E501
    """get_outgoing_connections

     # noqa: E501


    :rtype: ApiResponseSortedSetOutgoingConnectionSummary
    """
    return 'do some magic!'


def remove_federate_ca_group(ca_id, group, direction):  # noqa: E501
    """remove_federate_ca_group

     # noqa: E501

    :param ca_id: 
    :type ca_id: str
    :param group: 
    :type group: str
    :param direction: 
    :type direction: str

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def remove_federate_group(federate_id, group, direction):  # noqa: E501
    """remove_federate_group

     # noqa: E501

    :param federate_id: 
    :type federate_id: str
    :param group: 
    :type group: str
    :param direction: 
    :type direction: str

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def remove_federate_group_map(federate_id, remote_group, local_group):  # noqa: E501
    """remove_federate_group_map

     # noqa: E501

    :param federate_id: 
    :type federate_id: str
    :param remote_group: 
    :type remote_group: str
    :param local_group: 
    :type local_group: str

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def save_federate_certificate_ca(body=None):  # noqa: E501
    """save_federate_certificate_ca

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = ApiFederatecertificatesBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def save_federate_group_configuration():  # noqa: E501
    """save_federate_group_configuration

     # noqa: E501


    :rtype: ApiResponseString
    """
    return 'do some magic!'


def update_federate_details(body):  # noqa: E501
    """update_federate_details

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseFederate
    """
    if connexion.request.is_json:
        body = Federate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
