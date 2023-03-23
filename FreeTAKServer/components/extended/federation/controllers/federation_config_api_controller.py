import connexion
import six

from swagger_server.models.api_response_boolean import ApiResponseBoolean  # noqa: E501
from swagger_server.models.api_response_federation_config_info import ApiResponseFederationConfigInfo  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.federation_config_info import FederationConfigInfo  # noqa: E501
from swagger_server import util


def get_federation_config():  # noqa: E501
    """get_federation_config

     # noqa: E501


    :rtype: ApiResponseFederationConfigInfo
    """
    return 'do some magic!'


def modify_federation_config(body):  # noqa: E501
    """modify_federation_config

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseString
    """
    if connexion.request.is_json:
        body = FederationConfigInfo.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def verify_federation_truststore():  # noqa: E501
    """verify_federation_truststore

     # noqa: E501


    :rtype: ApiResponseBoolean
    """
    return 'do some magic!'
