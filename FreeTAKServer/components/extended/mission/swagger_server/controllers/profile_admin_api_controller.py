import connexion
import six

from swagger_server.models.api_response_list_profile import ApiResponseListProfile  # noqa: E501
from swagger_server.models.api_response_list_profile_directory import ApiResponseListProfileDirectory  # noqa: E501
from swagger_server.models.api_response_list_profile_file import ApiResponseListProfileFile  # noqa: E501
from swagger_server.models.api_response_list_string import ApiResponseListString  # noqa: E501
from swagger_server.models.api_response_profile import ApiResponseProfile  # noqa: E501
from swagger_server.models.api_response_profile_file import ApiResponseProfileFile  # noqa: E501
from swagger_server.models.name_file_body import NameFileBody  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server import util


def add_file(body, filename, name):  # noqa: E501
    """add_file

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param filename: 
    :type filename: str
    :param name: 
    :type name: str

    :rtype: ApiResponseProfileFile
    """
    if connexion.request.is_json:
        body = NameFileBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_profile(name, group=None):  # noqa: E501
    """create_profile

     # noqa: E501

    :param name: 
    :type name: str
    :param group: 
    :type group: List[str]

    :rtype: str
    """
    return 'do some magic!'


def delete_directories(name):  # noqa: E501
    """delete_directories

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: str
    """
    return 'do some magic!'


def delete_file(name, id):  # noqa: E501
    """delete_file

     # noqa: E501

    :param name: 
    :type name: str
    :param id: 
    :type id: int

    :rtype: str
    """
    return 'do some magic!'


def delete_profile(id):  # noqa: E501
    """delete_profile

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: str
    """
    return 'do some magic!'


def get_all_profile():  # noqa: E501
    """get_all_profile

     # noqa: E501


    :rtype: ApiResponseListProfile
    """
    return 'do some magic!'


def get_directories(name):  # noqa: E501
    """get_directories

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseListProfileDirectory
    """
    return 'do some magic!'


def get_file1(name, id):  # noqa: E501
    """get_file1

     # noqa: E501

    :param name: 
    :type name: str
    :param id: 
    :type id: int

    :rtype: List[bytearray]
    """
    return 'do some magic!'


def get_files(name):  # noqa: E501
    """get_files

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseListProfileFile
    """
    return 'do some magic!'


def get_profile(name):  # noqa: E501
    """get_profile

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseProfile
    """
    return 'do some magic!'


def get_valid_directories():  # noqa: E501
    """get_valid_directories

     # noqa: E501


    :rtype: ApiResponseListString
    """
    return 'do some magic!'


def send_profile(body, name):  # noqa: E501
    """send_profile

     # noqa: E501

    :param body: 
    :type body: List[]
    :param name: 
    :type name: str

    :rtype: str
    """
    return 'do some magic!'


def update_directories(name, directories):  # noqa: E501
    """update_directories

     # noqa: E501

    :param name: 
    :type name: str
    :param directories: 
    :type directories: List[str]

    :rtype: str
    """
    return 'do some magic!'


def update_profile(body, name):  # noqa: E501
    """update_profile

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param name: 
    :type name: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = Profile.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
