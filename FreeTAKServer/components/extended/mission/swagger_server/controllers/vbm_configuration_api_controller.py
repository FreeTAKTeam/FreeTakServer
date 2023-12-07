import connexion
import six

from swagger_server.models.vbm_configuration_model import VBMConfigurationModel  # noqa: E501
from swagger_server import util


def get_vbm_configuration():  # noqa: E501
    """get_vbm_configuration

     # noqa: E501


    :rtype: VBMConfigurationModel
    """
    return 'do some magic!'


def set_vbm_configuration(body):  # noqa: E501
    """set_vbm_configuration

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = VBMConfigurationModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
