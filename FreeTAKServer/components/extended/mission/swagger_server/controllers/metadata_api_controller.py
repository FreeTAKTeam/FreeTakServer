import connexion
import six

from swagger_server import util


def set_expiration(hash, expiration):  # noqa: E501
    """set_expiration

     # noqa: E501

    :param hash: 
    :type hash: str
    :param expiration: 
    :type expiration: int

    :rtype: str
    """
    return 'do some magic!'


def set_metadata(body, hash, metadata):  # noqa: E501
    """set_metadata

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param hash: 
    :type hash: str
    :param metadata: 
    :type metadata: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def set_metadata_keywords(body, hash):  # noqa: E501
    """set_metadata_keywords

     # noqa: E501

    :param body: 
    :type body: List[]
    :param hash: 
    :type hash: str

    :rtype: str
    """
    return 'do some magic!'
