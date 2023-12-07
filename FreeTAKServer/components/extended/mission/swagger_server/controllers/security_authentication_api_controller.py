import connexion
import six

from swagger_server.models.api_response_authentication_config_info import ApiResponseAuthenticationConfigInfo  # noqa: E501
from swagger_server.models.api_response_security_config_info import ApiResponseSecurityConfigInfo  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.authentication_config_info import AuthenticationConfigInfo  # noqa: E501
from swagger_server.models.security_config_info import SecurityConfigInfo  # noqa: E501
from swagger_server import util


def get_auth_config():  # noqa: E501
    """get_auth_config

     # noqa: E501


    :rtype: ApiResponseAuthenticationConfigInfo
    """
    return 'do some magic!'


def get_sec_config():  # noqa: E501
    """get_sec_config

     # noqa: E501


    :rtype: ApiResponseSecurityConfigInfo
    """
    return 'do some magic!'


def is_secure():  # noqa: E501
    """is_secure

     # noqa: E501


    :rtype: ApiResponseString
    """
    return 'do some magic!'


def modify_auth_config(body):  # noqa: E501
    """modify_auth_config

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = AuthenticationConfigInfo.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def modify_sec_config(body):  # noqa: E501
    """modify_sec_config

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = SecurityConfigInfo.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def test_auth_config():  # noqa: E501
    """test_auth_config

     # noqa: E501


    :rtype: ApiResponseString
    """
    return 'do some magic!'


def verify_config():  # noqa: E501
    """verify_config

     # noqa: E501


    :rtype: ApiResponseString
    """
    return 'do some magic!'
