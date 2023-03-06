import connexion
import six

from swagger_server.models.api_citrap_body import ApiCitrapBody  # noqa: E501
from swagger_server.models.citrap_id_body import CitrapIdBody  # noqa: E501
from swagger_server.models.id_attachment_body import IdAttachmentBody  # noqa: E501
from swagger_server import util


def add_attachment(body, client_uid, id):  # noqa: E501
    """add_attachment

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str
    :param id: 
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = IdAttachmentBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_report(id, client_uid):  # noqa: E501
    """delete_report

     # noqa: E501

    :param id: 
    :type id: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def get_report(id, client_uid):  # noqa: E501
    """get_report

     # noqa: E501

    :param id: 
    :type id: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'


def post_report(body, client_uid):  # noqa: E501
    """post_report

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = ApiCitrapBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def put_report(body, client_uid, id):  # noqa: E501
    """put_report

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param client_uid: 
    :type client_uid: str
    :param id: 
    :type id: str

    :rtype: str
    """
    if connexion.request.is_json:
        body = CitrapIdBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def search_reports(keywords=None, bbox=None, start_time=None, end_time=None, max_report_count=None, type=None, callsign=None, subscribe=None, client_uid=None):  # noqa: E501
    """search_reports

     # noqa: E501

    :param keywords: 
    :type keywords: str
    :param bbox: 
    :type bbox: str
    :param start_time: 
    :type start_time: str
    :param end_time: 
    :type end_time: str
    :param max_report_count: 
    :type max_report_count: str
    :param type: 
    :type type: str
    :param callsign: 
    :type callsign: str
    :param subscribe: 
    :type subscribe: str
    :param client_uid: 
    :type client_uid: str

    :rtype: str
    """
    return 'do some magic!'
