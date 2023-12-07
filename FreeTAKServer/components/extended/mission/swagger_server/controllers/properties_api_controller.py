import connexion
import six

from swagger_server.models.api_response_collection_string import ApiResponseCollectionString  # noqa: E501
from swagger_server.models.api_response_entry_string_string import ApiResponseEntryStringString  # noqa: E501
from swagger_server.models.api_response_map_string_collection_string import ApiResponseMapStringCollectionString  # noqa: E501
from swagger_server.models.properties_uid_body import PropertiesUidBody  # noqa: E501
from swagger_server import util


def clear_all_property(uid):  # noqa: E501
    """clear_all_property

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: None
    """
    return 'do some magic!'


def clear_property(uid, key):  # noqa: E501
    """clear_property

     # noqa: E501

    :param uid: 
    :type uid: str
    :param key: 
    :type key: str

    :rtype: None
    """
    return 'do some magic!'


def get_all_property_for_uid(uid):  # noqa: E501
    """get_all_property_for_uid

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: ApiResponseMapStringCollectionString
    """
    return 'do some magic!'


def get_all_property_keys():  # noqa: E501
    """get_all_property_keys

     # noqa: E501


    :rtype: ApiResponseCollectionString
    """
    return 'do some magic!'


def get_property_for_uid(uid, key):  # noqa: E501
    """get_property_for_uid

     # noqa: E501

    :param uid: 
    :type uid: str
    :param key: 
    :type key: str

    :rtype: ApiResponseCollectionString
    """
    return 'do some magic!'


def store_property(body, uid):  # noqa: E501
    """store_property

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param uid: 
    :type uid: str

    :rtype: ApiResponseEntryStringString
    """
    if connexion.request.is_json:
        body = PropertiesUidBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
