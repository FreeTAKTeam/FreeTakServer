import connexion
import six

from swagger_server.models.uid_filename_body import UidFilenameBody  # noqa: E501
from swagger_server import util


def get_file(uid, filename):  # noqa: E501
    """get_file

     # noqa: E501

    :param uid: 
    :type uid: str
    :param filename: 
    :type filename: str

    :rtype: str
    """
    return 'do some magic!'


def put_file(body, uid, filename):  # noqa: E501
    """put_file

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param uid: 
    :type uid: str
    :param filename: 
    :type filename: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = UidFilenameBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
