import connexion
import six

from swagger_server.models.api_response_list_token_result import ApiResponseListTokenResult  # noqa: E501
from swagger_server import util


def get_all(expired=None):  # noqa: E501
    """get_all

     # noqa: E501

    :param expired: 
    :type expired: bool

    :rtype: ApiResponseListTokenResult
    """
    return 'do some magic!'


def revoke_token(token):  # noqa: E501
    """revoke_token

     # noqa: E501

    :param token: 
    :type token: str

    :rtype: None
    """
    return 'do some magic!'


def revoke_tokens(tokens):  # noqa: E501
    """revoke_tokens

     # noqa: E501

    :param tokens: 
    :type tokens: str

    :rtype: None
    """
    return 'do some magic!'
