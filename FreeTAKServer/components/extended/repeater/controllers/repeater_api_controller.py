import connexion
import six

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_integer import ApiResponseInteger  # noqa: E501
from swagger_server.models.api_response_list_repeatable import ApiResponseListRepeatable  # noqa: E501
from swagger_server import util


def get_list():  # noqa: E501
    """get_list

     # noqa: E501


    :rtype: ApiResponseListRepeatable
    """
    return 'do some magic!'


def get_period():  # noqa: E501
    """get_period

     # noqa: E501


    :rtype: ApiResponseInteger
    """
    return 'do some magic!'


def remove(uid):  # noqa: E501
    """remove

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def set_period(body):  # noqa: E501
    """set_period

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = int.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
