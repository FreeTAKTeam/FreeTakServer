import connexion
import six

from swagger_server.models.group_name_model import GroupNameModel  # noqa: E501
from swagger_server.models.new_user_model import NewUserModel  # noqa: E501
from swagger_server.models.simple_group_with_users_model import SimpleGroupWithUsersModel  # noqa: E501
from swagger_server.models.simple_user_group_model import SimpleUserGroupModel  # noqa: E501
from swagger_server.models.user_generation_in_bulk_model import UserGenerationInBulkModel  # noqa: E501
from swagger_server.models.user_password_model import UserPasswordModel  # noqa: E501
from swagger_server.models.username_model import UsernameModel  # noqa: E501
from swagger_server import util


def change_user_password(body):  # noqa: E501
    """change_user_password

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = UserPasswordModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_file_users_in_bulk(body):  # noqa: E501
    """create_file_users_in_bulk

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[UserPasswordModel]
    """
    if connexion.request.is_json:
        body = UserGenerationInBulkModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_or_update_file_user(body):  # noqa: E501
    """create_or_update_file_user

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = NewUserModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_user(username):  # noqa: E501
    """delete_user

     # noqa: E501

    :param username: 
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def get_all_group_names():  # noqa: E501
    """get_all_group_names

     # noqa: E501


    :rtype: List[GroupNameModel]
    """
    return 'do some magic!'


def get_all_users():  # noqa: E501
    """get_all_users

     # noqa: E501


    :rtype: List[UsernameModel]
    """
    return 'do some magic!'


def get_groups_for_users(username):  # noqa: E501
    """get_groups_for_users

     # noqa: E501

    :param username: 
    :type username: str

    :rtype: SimpleUserGroupModel
    """
    return 'do some magic!'


def get_users_in_group(group):  # noqa: E501
    """get_users_in_group

     # noqa: E501

    :param group: 
    :type group: str

    :rtype: SimpleGroupWithUsersModel
    """
    return 'do some magic!'


def update_groups_for_user(body):  # noqa: E501
    """update_groups_for_user

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = SimpleUserGroupModel.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
