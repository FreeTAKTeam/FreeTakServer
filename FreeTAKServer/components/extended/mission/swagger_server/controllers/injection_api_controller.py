import connexion
import six

from swagger_server.models.api_response_collection_injector_config import ApiResponseCollectionInjectorConfig  # noqa: E501
from swagger_server.models.api_response_set_injector_config import ApiResponseSetInjectorConfig  # noqa: E501
from swagger_server.models.injector_config import InjectorConfig  # noqa: E501
from swagger_server import util


def delete_injector(uid, to_inject):  # noqa: E501
    """delete_injector

     # noqa: E501

    :param uid: 
    :type uid: str
    :param to_inject: 
    :type to_inject: str

    :rtype: ApiResponseSetInjectorConfig
    """
    return 'do some magic!'


def get_all_cot_injectors():  # noqa: E501
    """get_all_cot_injectors

     # noqa: E501


    :rtype: ApiResponseSetInjectorConfig
    """
    return 'do some magic!'


def get_one_cot_injector(uid):  # noqa: E501
    """get_one_cot_injector

     # noqa: E501

    :param uid: 
    :type uid: str

    :rtype: ApiResponseCollectionInjectorConfig
    """
    return 'do some magic!'


def put_cot_injector(body):  # noqa: E501
    """put_cot_injector

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseSetInjectorConfig
    """
    if connexion.request.is_json:
        body = InjectorConfig.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
