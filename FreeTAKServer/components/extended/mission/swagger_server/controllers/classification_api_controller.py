import connexion
import six

from swagger_server.models.api_response_caveat import ApiResponseCaveat  # noqa: E501
from swagger_server.models.api_response_classification import ApiResponseClassification  # noqa: E501
from swagger_server.models.api_response_list_caveat import ApiResponseListCaveat  # noqa: E501
from swagger_server.models.api_response_list_classification import ApiResponseListClassification  # noqa: E501
from swagger_server.models.api_response_long import ApiResponseLong  # noqa: E501
from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server import util


def delete_caveat(name):  # noqa: E501
    """delete_caveat

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseLong
    """
    return 'do some magic!'


def delete_classification(level):  # noqa: E501
    """delete_classification

     # noqa: E501

    :param level: 
    :type level: str

    :rtype: ApiResponseLong
    """
    return 'do some magic!'


def get_all_caveat():  # noqa: E501
    """get_all_caveat

     # noqa: E501


    :rtype: ApiResponseListCaveat
    """
    return 'do some magic!'


def get_all_classifications():  # noqa: E501
    """get_all_classifications

     # noqa: E501


    :rtype: ApiResponseListClassification
    """
    return 'do some magic!'


def get_classification_for_level(level):  # noqa: E501
    """get_classification_for_level

     # noqa: E501

    :param level: 
    :type level: str

    :rtype: ApiResponseClassification
    """
    return 'do some magic!'


def new_caveat(name):  # noqa: E501
    """new_caveat

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseCaveat
    """
    return 'do some magic!'


def new_classification(level):  # noqa: E501
    """new_classification

     # noqa: E501

    :param level: 
    :type level: str

    :rtype: ApiResponseClassification
    """
    return 'do some magic!'


def set_caveats_for_classification(body):  # noqa: E501
    """set_caveats_for_classification

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseClassification
    """
    if connexion.request.is_json:
        body = Classification.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
