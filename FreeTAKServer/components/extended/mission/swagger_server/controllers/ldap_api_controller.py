import connexion
import six

from swagger_server.models.api_response_integer import ApiResponseInteger  # noqa: E501
from swagger_server.models.api_response_sorted_set_ldap_group import ApiResponseSortedSetLdapGroup  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server import util


def get_group_prefix():  # noqa: E501
    """get_group_prefix

     # noqa: E501


    :rtype: ApiResponseString
    """
    return 'do some magic!'


def get_ldap_group_members(group_name_filter):  # noqa: E501
    """get_ldap_group_members

     # noqa: E501

    :param group_name_filter: 
    :type group_name_filter: List[str]

    :rtype: ApiResponseInteger
    """
    return 'do some magic!'


def get_ldap_groups(group_name_filter):  # noqa: E501
    """get_ldap_groups

     # noqa: E501

    :param group_name_filter: 
    :type group_name_filter: str

    :rtype: ApiResponseSortedSetLdapGroup
    """
    return 'do some magic!'
