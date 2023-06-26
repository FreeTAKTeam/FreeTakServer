import connexion
import six

from swagger_server.models.video_collections import VideoCollections  # noqa: E501
from swagger_server.models.video_connection import VideoConnection  # noqa: E501
from swagger_server import util


def create_video_connection(body):  # noqa: E501
    """create_video_connection

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = VideoCollections.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_video_connection(uid):  # noqa: E501
    """delete_video_connection

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: None
    """
    return 'do some magic!'


def get_video_collections(protocol=None):  # noqa: E501
    """get_video_collections

     # noqa: E501

    :param protocol: 
    :type protocol: str

    :rtype: VideoCollections
    """
    return 'do some magic!'


def get_video_connection(uid):  # noqa: E501
    """get_video_connection

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: VideoConnection
    """
    return 'do some magic!'


def update_video_connection(body, uid):  # noqa: E501
    """update_video_connection

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param uid: 
    :type uid: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = VideoConnection.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
