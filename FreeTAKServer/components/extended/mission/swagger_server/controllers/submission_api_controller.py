import connexion
import six

from swagger_server.models.api_response_connection_modify_result import ApiResponseConnectionModifyResult  # noqa: E501
from swagger_server.models.api_response_data_feed import ApiResponseDataFeed  # noqa: E501
from swagger_server.models.api_response_input import ApiResponseInput  # noqa: E501
from swagger_server.models.api_response_input_metric import ApiResponseInputMetric  # noqa: E501
from swagger_server.models.api_response_list_data_feed import ApiResponseListDataFeed  # noqa: E501
from swagger_server.models.api_response_map_string_integer import ApiResponseMapStringInteger  # noqa: E501
from swagger_server.models.api_response_messaging_config_info import ApiResponseMessagingConfigInfo  # noqa: E501
from swagger_server.models.api_response_sorted_set_input_metric import ApiResponseSortedSetInputMetric  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.data_feed import DataFeed  # noqa: E501
from swagger_server.models.input import Input  # noqa: E501
from swagger_server.models.messaging_config_info import MessagingConfigInfo  # noqa: E501
from swagger_server import util


def create_data_feed(body):  # noqa: E501
    """create_data_feed

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseDataFeed
    """
    if connexion.request.is_json:
        body = DataFeed.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_input(body):  # noqa: E501
    """create_input

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseInput
    """
    if connexion.request.is_json:
        body = Input.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_data_feed(name):  # noqa: E501
    """delete_data_feed

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseDataFeed
    """
    return 'do some magic!'


def delete_input(name):  # noqa: E501
    """delete_input

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseInput
    """
    return 'do some magic!'


def disable_store_forward_chat():  # noqa: E501
    """disable_store_forward_chat

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def enable_store_forward_chat():  # noqa: E501
    """enable_store_forward_chat

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def get_config_info():  # noqa: E501
    """get_config_info

     # noqa: E501


    :rtype: ApiResponseMessagingConfigInfo
    """
    return 'do some magic!'


def get_data_feed(name):  # noqa: E501
    """get_data_feed

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseDataFeed
    """
    return 'do some magic!'


def get_data_feeds():  # noqa: E501
    """get_data_feeds

     # noqa: E501


    :rtype: ApiResponseListDataFeed
    """
    return 'do some magic!'


def get_database_cot_counts():  # noqa: E501
    """get_database_cot_counts

     # noqa: E501


    :rtype: ApiResponseMapStringInteger
    """
    return 'do some magic!'


def get_input_metric(name):  # noqa: E501
    """get_input_metric

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseInputMetric
    """
    return 'do some magic!'


def get_input_metrics(exclude_data_feeds=None):  # noqa: E501
    """get_input_metrics

     # noqa: E501

    :param exclude_data_feeds: 
    :type exclude_data_feeds: bool

    :rtype: ApiResponseSortedSetInputMetric
    """
    return 'do some magic!'


def is_store_forward_chat_enabled():  # noqa: E501
    """is_store_forward_chat_enabled

     # noqa: E501


    :rtype: bool
    """
    return 'do some magic!'


def modify_config_info(body):  # noqa: E501
    """modify_config_info

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = MessagingConfigInfo.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def modify_data_feed(body, name):  # noqa: E501
    """modify_data_feed

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param name: 
    :type name: str

    :rtype: ApiResponseDataFeed
    """
    if connexion.request.is_json:
        body = DataFeed.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def modify_input(body, id):  # noqa: E501
    """modify_input

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: 
    :type id: str

    :rtype: ApiResponseConnectionModifyResult
    """
    if connexion.request.is_json:
        body = Input.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
