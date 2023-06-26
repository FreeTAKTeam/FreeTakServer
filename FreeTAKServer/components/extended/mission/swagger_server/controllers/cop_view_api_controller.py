import connexion
import six

from swagger_server.models.api_response_list_mission import ApiResponseListMission  # noqa: E501
from swagger_server.models.api_response_set_cop_hierarchy_node import ApiResponseSetCopHierarchyNode  # noqa: E501
from swagger_server import util


def get_all_cop_missions(path=None, offset=None, size=None):  # noqa: E501
    """get_all_cop_missions

     # noqa: E501

    :param path: 
    :type path: str
    :param offset: 
    :type offset: int
    :param size: 
    :type size: int

    :rtype: ApiResponseListMission
    """
    return 'do some magic!'


def get_hierarchy():  # noqa: E501
    """get_hierarchy

     # noqa: E501


    :rtype: ApiResponseSetCopHierarchyNode
    """
    return 'do some magic!'
