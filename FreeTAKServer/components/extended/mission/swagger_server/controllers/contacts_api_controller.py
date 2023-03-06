import connexion
import six

from swagger_server.models.remote_subscription import RemoteSubscription  # noqa: E501
from swagger_server import util


def get_all_contacts(sort_by=None, direction=None, no_federates=None):  # noqa: E501
    """get_all_contacts

     # noqa: E501

    :param sort_by: 
    :type sort_by: str
    :param direction: 
    :type direction: str
    :param no_federates: 
    :type no_federates: bool

    :rtype: List[RemoteSubscription]
    """
    return 'do some magic!'
