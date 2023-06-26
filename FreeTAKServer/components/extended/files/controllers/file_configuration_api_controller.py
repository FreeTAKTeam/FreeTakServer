import connexion
import six

from swagger_server.models.file_configuration_model import FileConfigurationModel  # noqa: E501
from swagger_server import util


def get_file_configuration():  # noqa: E501
    """get_file_configuration

     # noqa: E501


    :rtype: FileConfigurationModel
    """
    return 'do some magic!'


def set_file_configuration(body):  # noqa: E501
    """set_file_configuration

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = FileConfigurationModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
