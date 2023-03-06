import connexion
import six

from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.name_submit_body import NameSubmitBody  # noqa: E501
from swagger_server.models.name_submit_body1 import NameSubmitBody1  # noqa: E501
from swagger_server.models.submit_result_body import SubmitResultBody  # noqa: E501
from swagger_server import util


def delete_from_plugin(name, all_request_params):  # noqa: E501
    """delete_from_plugin

     # noqa: E501

    :param name: 
    :type name: str
    :param all_request_params: 
    :type all_request_params: Dict[str, str]

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def request_from_plugin(name, all_request_params):  # noqa: E501
    """request_from_plugin

     # noqa: E501

    :param name: 
    :type name: str
    :param all_request_params: 
    :type all_request_params: Dict[str, str]

    :rtype: str
    """
    return 'do some magic!'


def submit_to_plugin_utf8(body, all_request_params, name):  # noqa: E501
    """submit_to_plugin_utf8

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param all_request_params: 
    :type all_request_params: Dict[str, str]
    :param name: 
    :type name: str

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = NameSubmitBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def submit_to_plugin_utf8_with_result(body, all_request_params, name):  # noqa: E501
    """submit_to_plugin_utf8_with_result

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param all_request_params: 
    :type all_request_params: Dict[str, str]
    :param name: 
    :type name: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = SubmitResultBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_in_plugin(body, all_request_params, name):  # noqa: E501
    """update_in_plugin

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param all_request_params: 
    :type all_request_params: Dict[str, str]
    :param name: 
    :type name: str

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = NameSubmitBody1.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
