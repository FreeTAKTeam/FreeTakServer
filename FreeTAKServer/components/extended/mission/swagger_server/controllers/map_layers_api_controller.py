import connexion
import six

from swagger_server.models.api_response_collection_map_layer import ApiResponseCollectionMapLayer  # noqa: E501
from swagger_server.models.api_response_map_layer import ApiResponseMapLayer  # noqa: E501
from swagger_server.models.map_layer import MapLayer  # noqa: E501
from swagger_server import util


def create_map_layer1(body):  # noqa: E501
    """create_map_layer1

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseMapLayer
    """
    if connexion.request.is_json:
        body = MapLayer.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_map_layer1(uid):  # noqa: E501
    """delete_map_layer1

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: None
    """
    return 'do some magic!'


def get_all_map_layers():  # noqa: E501
    """get_all_map_layers

     # noqa: E501


    :rtype: ApiResponseCollectionMapLayer
    """
    return 'do some magic!'


def get_map_layer_for_uid(uid):  # noqa: E501
    """get_map_layer_for_uid

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: ApiResponseMapLayer
    """
    return 'do some magic!'


def update_map_layer1(body):  # noqa: E501
    """update_map_layer1

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseMapLayer
    """
    if connexion.request.is_json:
        body = MapLayer.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
