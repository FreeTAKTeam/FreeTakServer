import connexion
import six

from swagger_server import util


def get_config():  # noqa: E501
    """get_config

     # noqa: E501


    :rtype: str
    """
    return 'do some magic!'


def make_key_store(cn=None, password=None):  # noqa: E501
    """make_key_store

     # noqa: E501

    :param cn: 
    :type cn: str
    :param password: 
    :type password: str

    :rtype: List[bytearray]
    """
    return 'do some magic!'


def sign_client_cert(body, client_uid=None, version=None):  # noqa: E501
    """sign_client_cert

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str
    :param version: 
    :type version: str

    :rtype: List[bytearray]
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def sign_client_cert_v2(body, client_uid=None, version=None):  # noqa: E501
    """sign_client_cert_v2

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str
    :param version: 
    :type version: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
