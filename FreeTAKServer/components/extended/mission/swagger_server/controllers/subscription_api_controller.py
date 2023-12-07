import connexion
import six

from swagger_server.models.api_response_set_subscription_info import ApiResponseSetSubscriptionInfo  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.api_response_subscription_info import ApiResponseSubscriptionInfo  # noqa: E501
from swagger_server.models.filter import Filter  # noqa: E501
from swagger_server.models.group import Group  # noqa: E501
from swagger_server.models.tmp_static_sub import TmpStaticSub  # noqa: E501
from swagger_server import util


def add_subscription(body):  # noqa: E501
    """add_subscription

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseSubscriptionInfo
    """
    if connexion.request.is_json:
        body = TmpStaticSub.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_filter(client_uid):  # noqa: E501
    """delete_filter

     # noqa: E501

    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def delete_subscription(uid):  # noqa: E501
    """delete_subscription

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def get_all_subscriptions(sort_by=None, direction=None, page=None, limit=None):  # noqa: E501
    """get_all_subscriptions

     # noqa: E501

    :param sort_by: 
    :type sort_by: str
    :param direction: 
    :type direction: str
    :param page: 
    :type page: int
    :param limit: 
    :type limit: int

    :rtype: ApiResponseSetSubscriptionInfo
    """
    return 'do some magic!'


def groups_updated(username):  # noqa: E501
    """groups_updated

     # noqa: E501

    :param username: 
    :type username: str

    :rtype: str
    """
    return 'do some magic!'


def set_active_groups(body, client_uid=None):  # noqa: E501
    """set_active_groups

     # noqa: E501

    :param body: 
    :type body: List[]
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def set_active_groups1(body, client_uid=None):  # noqa: E501
    """set_active_groups1

     # noqa: E501

    :param body: 
    :type body: list | bytes
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = [Group.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def set_filter(body, client_uid):  # noqa: E501
    """set_filter

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = Filter.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def toggle_incognito(uid):  # noqa: E501
    """toggle_incognito

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: str
    """
    return 'do some magic!'
