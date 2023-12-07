import connexion
import six

from swagger_server.models.api_iconset_body import ApiIconsetBody  # noqa: E501
from swagger_server.models.api_response_list_string import ApiResponseListString  # noqa: E501
from swagger_server.models.api_response_set_string import ApiResponseSetString  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server import util


def get_all_icon_urls_for_iconset(uid):  # noqa: E501
    """get_all_icon_urls_for_iconset

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: ApiResponseListString
    """
    return 'do some magic!'


def get_all_iconset_uids():  # noqa: E501
    """get_all_iconset_uids

     # noqa: E501


    :rtype: ApiResponseSetString
    """
    return 'do some magic!'


def get_icon(uid, group, name):  # noqa: E501
    """get_icon

     # noqa: E501

    :param uid: 
    :type uid: str
    :param group: 
    :type group: str
    :param name: 
    :type name: str

    :rtype: List[bytearray]
    """
    return 'do some magic!'


def get_icon_image(iconsetpath=None, cot_type=None, medevac=None, group_name=None, role=None, color=None, relative=None):  # noqa: E501
    """get_icon_image

     # noqa: E501

    :param iconsetpath: 
    :type iconsetpath: str
    :param cot_type: 
    :type cot_type: str
    :param medevac: 
    :type medevac: bool
    :param group_name: 
    :type group_name: str
    :param role: 
    :type role: str
    :param color: 
    :type color: int
    :param relative: 
    :type relative: bool

    :rtype: List[bytearray]
    """
    return 'do some magic!'


def get_icon_url(iconsetpath=None, cot_type=None, medevac=None, group_name=None, role=None, color=None, relative=None):  # noqa: E501
    """get_icon_url

     # noqa: E501

    :param iconsetpath: 
    :type iconsetpath: str
    :param cot_type: 
    :type cot_type: str
    :param medevac: 
    :type medevac: bool
    :param group_name: 
    :type group_name: str
    :param role: 
    :type role: str
    :param color: 
    :type color: int
    :param relative: 
    :type relative: bool

    :rtype: str
    """
    return 'do some magic!'


def post_iconset_zip(body=None):  # noqa: E501
    """post_iconset_zip

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = ApiIconsetBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
