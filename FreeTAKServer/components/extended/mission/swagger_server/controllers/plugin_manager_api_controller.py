import connexion
import six

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_collection_plugin_info import ApiResponseCollectionPluginInfo  # noqa: E501
from swagger_server import util


def change_all_plugin_started_status(status):  # noqa: E501
    """change_all_plugin_started_status

     # noqa: E501

    :param status: 
    :type status: bool

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def change_plugin_archive_setting(name, archive_enabled):  # noqa: E501
    """change_plugin_archive_setting

     # noqa: E501

    :param name: 
    :type name: str
    :param archive_enabled: 
    :type archive_enabled: bool

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def change_plugin_enabled_setting(name, status):  # noqa: E501
    """change_plugin_enabled_setting

     # noqa: E501

    :param name: 
    :type name: str
    :param status: 
    :type status: bool

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def change_plugin_started_status(name, status):  # noqa: E501
    """change_plugin_started_status

     # noqa: E501

    :param name: 
    :type name: str
    :param status: 
    :type status: bool

    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def get_all_plugin_info():  # noqa: E501
    """get_all_plugin_info

     # noqa: E501


    :rtype: ApiResponseCollectionPluginInfo
    """
    return 'do some magic!'
