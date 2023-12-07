import connexion
import six

from swagger_server.models.api_response_entry_integer_integer import ApiResponseEntryIntegerInteger  # noqa: E501
from swagger_server.models.api_response_qos import ApiResponseQos  # noqa: E501
from swagger_server import util


def enable_delivery(body):  # noqa: E501
    """enable_delivery

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = bool.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def enable_dos(body):  # noqa: E501
    """enable_dos

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = bool.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def enable_read(body):  # noqa: E501
    """enable_read

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = bool.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_active_delivery_rate_limit():  # noqa: E501
    """get_active_delivery_rate_limit

     # noqa: E501


    :rtype: ApiResponseEntryIntegerInteger
    """
    return 'do some magic!'


def get_active_dos_rate_limit():  # noqa: E501
    """get_active_dos_rate_limit

     # noqa: E501


    :rtype: ApiResponseEntryIntegerInteger
    """
    return 'do some magic!'


def get_active_read_rate_limit():  # noqa: E501
    """get_active_read_rate_limit

     # noqa: E501


    :rtype: ApiResponseEntryIntegerInteger
    """
    return 'do some magic!'


def get_qos_conf():  # noqa: E501
    """get_qos_conf

     # noqa: E501


    :rtype: ApiResponseQos
    """
    return 'do some magic!'
