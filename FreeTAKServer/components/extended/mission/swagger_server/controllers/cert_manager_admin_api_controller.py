import connexion
import six

from swagger_server.models.api_response_list_tak_cert import ApiResponseListTakCert  # noqa: E501
from swagger_server.models.api_response_tak_cert import ApiResponseTakCert  # noqa: E501
from swagger_server import util


def delete_certificates(ids):  # noqa: E501
    """delete_certificates

     # noqa: E501

    :param ids: 
    :type ids: str

    :rtype: str
    """
    return 'do some magic!'


def download_certificate(hash):  # noqa: E501
    """download_certificate

     # noqa: E501

    :param hash: 
    :type hash: str

    :rtype: str
    """
    return 'do some magic!'


def download_certificates(ids):  # noqa: E501
    """download_certificates

     # noqa: E501

    :param ids: 
    :type ids: str

    :rtype: List[bytearray]
    """
    return 'do some magic!'


def get_active():  # noqa: E501
    """get_active

     # noqa: E501


    :rtype: ApiResponseListTakCert
    """
    return 'do some magic!'


def get_all1(username=None):  # noqa: E501
    """get_all1

     # noqa: E501

    :param username: 
    :type username: str

    :rtype: ApiResponseListTakCert
    """
    return 'do some magic!'


def get_certificate(hash):  # noqa: E501
    """get_certificate

     # noqa: E501

    :param hash: 
    :type hash: str

    :rtype: ApiResponseTakCert
    """
    return 'do some magic!'


def get_expired():  # noqa: E501
    """get_expired

     # noqa: E501


    :rtype: ApiResponseListTakCert
    """
    return 'do some magic!'


def get_replaced():  # noqa: E501
    """get_replaced

     # noqa: E501


    :rtype: ApiResponseListTakCert
    """
    return 'do some magic!'


def get_revoked():  # noqa: E501
    """get_revoked

     # noqa: E501


    :rtype: ApiResponseListTakCert
    """
    return 'do some magic!'


def revoke_certificate(hash):  # noqa: E501
    """revoke_certificate

     # noqa: E501

    :param hash: 
    :type hash: str

    :rtype: ApiResponseTakCert
    """
    return 'do some magic!'


def revoke_certificates(ids):  # noqa: E501
    """revoke_certificates

     # noqa: E501

    :param ids: 
    :type ids: str

    :rtype: str
    """
    return 'do some magic!'
