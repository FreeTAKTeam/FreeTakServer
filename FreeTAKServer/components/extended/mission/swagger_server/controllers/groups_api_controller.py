import connexion
import six

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_collection_group import ApiResponseCollectionGroup  # noqa: E501
from swagger_server.models.api_response_group import ApiResponseGroup  # noqa: E501
from swagger_server.models.api_response_sorted_set_user import ApiResponseSortedSetUser  # noqa: E501
from swagger_server.models.api_response_user_groups import ApiResponseUserGroups  # noqa: E501
from swagger_server import util


def get_all_groups(use_cache=None, send_latest_sa=None):  # noqa: E501
    """get_all_groups

     # noqa: E501

    :param use_cache: 
    :type use_cache: bool
    :param send_latest_sa: 
    :type send_latest_sa: bool

    :rtype: ApiResponseCollectionGroup
    """
    return 'do some magic!'


def get_all_users2():  # noqa: E501
    """get_all_users2

     # noqa: E501


    :rtype: ApiResponseSortedSetUser
    """
    return 'do some magic!'


def get_group(name, direction):  # noqa: E501
    """get_group

     # noqa: E501

    :param name: 
    :type name: str
    :param direction: 
    :type direction: str

    :rtype: ApiResponseGroup
    """
    return 'do some magic!'


def get_group_cache_enabled():  # noqa: E501
    """get_group_cache_enabled

     # noqa: E501


    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'


def get_user(connection_id):  # noqa: E501
    """get_user

     # noqa: E501

    :param connection_id: 
    :type connection_id: str

    :rtype: ApiResponseUserGroups
    """
    return 'do some magic!'
