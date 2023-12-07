import connexion
import six

from swagger_server.models.api_response_list_client_endpoint import ApiResponseListClientEndpoint  # noqa: E501
from swagger_server import util


def get_client_endpoints(sec_ago=None, show_currently_connected_clients=None, show_most_recent_only=None):  # noqa: E501
    """get_client_endpoints

     # noqa: E501

    :param sec_ago: 
    :type sec_ago: int
    :param show_currently_connected_clients: 
    :type show_currently_connected_clients: str
    :param show_most_recent_only: 
    :type show_most_recent_only: str

    :rtype: ApiResponseListClientEndpoint
    """
    return 'do some magic!'
