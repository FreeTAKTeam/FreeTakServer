import connexion
import six

from swagger_server.models.tak_user import TAKUser  # noqa: E501
from swagger_server import util


def confirm(token):  # noqa: E501
    """confirm

     # noqa: E501

    :param token: 
    :type token: str

    :rtype: None
    """
    return 'do some magic!'


def get_all_users1():  # noqa: E501
    """get_all_users1

     # noqa: E501


    :rtype: List[TAKUser]
    """
    return 'do some magic!'


def invite(email_address, group=None):  # noqa: E501
    """invite

     # noqa: E501

    :param email_address: 
    :type email_address: str
    :param group: 
    :type group: List[str]

    :rtype: None
    """
    return 'do some magic!'


def sign_up(email_address, token):  # noqa: E501
    """sign_up

     # noqa: E501

    :param email_address: 
    :type email_address: str
    :param token: 
    :type token: str

    :rtype: None
    """
    return 'do some magic!'
